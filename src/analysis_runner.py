"""Run the slate strategy + the post-autopsy learning loop in-app via headless
Claude Code.

The Slate Strategy tab's button calls `run_analysis`, and the Autopsy tab's
buttons call `run_autopsy_review` / `run_apply_proposals`. Each shells out to the
`claude` CLI in headless print mode (`claude -p`), pointed at this repo, to read
the bundle + referenced files and write an output file per the CLAUDE.md workflow.

This uses the user's existing Claude Code subscription auth — no API key, no
separate billing. The `claude` binary is already installed on the machine.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from src.bundle import build_bundle

_REPO_ROOT = Path(__file__).parent.parent
_TIMEOUT_S = 1200  # generous ceiling for reading many article PDFs/images


def _claude_binary() -> str | None:
    """Resolve the claude CLI path; Streamlit's PATH may not include ~/.local/bin."""
    found = shutil.which("claude")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / "claude"
    return str(fallback) if fallback.exists() else None


def _run_claude(prompt: str, out_path: Path) -> dict:
    """Run `claude -p` headlessly and confirm `out_path` was freshly written.

    Returns {ok, error, duration_s, cost_usd}.
    """
    started = time.time()

    binary = _claude_binary()
    if not binary:
        return {"ok": False, "error": "Couldn't find the `claude` CLI on this machine.",
                "duration_s": 0.0, "cost_usd": None}

    # Snapshot the prior file (mtime for the fresh-write check, bytes so a
    # FAILED run that half-wrote the file never leaves a partial strategy
    # rendering as if it were current — we roll back to the pre-run version).
    prior_mtime = out_path.stat().st_mtime if out_path.exists() else None
    prior_bytes = out_path.read_bytes() if out_path.exists() else None

    def _rollback_partial():
        """On failure: undo any partial write claude left behind."""
        try:
            if not out_path.exists():
                return
            if out_path.stat().st_mtime == prior_mtime:
                return  # untouched
            if prior_bytes is None:
                out_path.unlink()  # didn't exist before the run
            else:
                out_path.write_bytes(prior_bytes)
        except OSError:
            pass  # rollback is best-effort; the error is reported regardless

    cmd = [
        binary, "-p", prompt,
        "--output-format", "json",
        "--permission-mode", "acceptEdits",
        "--allowedTools", "Read,Glob,Grep,Write,Edit",
    ]

    try:
        proc = subprocess.run(
            cmd, cwd=str(_REPO_ROOT),
            capture_output=True, text=True, timeout=_TIMEOUT_S,
        )
    except subprocess.TimeoutExpired:
        _rollback_partial()
        return {"ok": False, "error": f"Timed out after {_TIMEOUT_S // 60} minutes.",
                "duration_s": time.time() - started, "cost_usd": None}

    duration = time.time() - started

    cost = None
    cli_error = None
    if proc.stdout.strip():
        try:
            data = json.loads(proc.stdout)
            cost = data.get("total_cost_usd")
            if data.get("is_error"):
                cli_error = data.get("result") or "Claude reported an error."
        except json.JSONDecodeError:
            pass

    if proc.returncode != 0 or cli_error:
        msg = cli_error or (proc.stderr.strip()[:500]) or f"claude exited with code {proc.returncode}."
        _rollback_partial()
        return {"ok": False, "error": msg, "duration_s": duration, "cost_usd": cost}

    # Confirm a fresh output file actually landed.
    if not out_path.exists() or out_path.stat().st_mtime == prior_mtime:
        return {"ok": False,
                "error": "Claude ran but didn't write the output file. Check the inputs and try again.",
                "duration_s": duration, "cost_usd": cost}

    return {"ok": True, "error": None, "duration_s": duration, "cost_usd": cost}


def run_analysis(slug: str, contest_label: str, sport: str) -> dict:
    """Build the bundle (articles + every loaded vendor projection) and run headless
    Claude to write the slate strategy to data/slate_analysis/<slug>.md."""
    out_path = _REPO_ROOT / "data" / "slate_analysis" / f"{slug}.md"
    bundle_path = build_bundle(slug, contest_label, sport)
    prompt = (
        f"Write the {contest_label} slate strategy from EVERYTHING uploaded for this slate — "
        f"the articles AND every vendor projection. "
        f"Read the bundle at `{bundle_path}`: this is MANDATORY — EVERY single slate-data file it "
        f"lists under `articles/{slug}/`, no exceptions (the article PDFs, notes/.txt/.md, data CSVs "
        f"read as text tables, AND every photo/screenshot/image — use the Read tool on images, it "
        f"reads them visually; do not skip a file because it looks redundant) AND the `## Projections` "
        f"tables in the bundle (every loaded vendor's ownership/projection numbers). Then read the "
        f"strategy docs the bundle references for sport `{sport}`: `rules/{slug}/philosophy.md`, "
        f"`rules/{slug}/framework.md`, `rules/{slug}/autopsies.md`, `rules/{slug}/lessons.yaml`, "
        f"`rules/shared/anchor_equivalence.md`, `rules/shared/sharp_playbook.md`, and the venue "
        f"file for this slate's venue (golf → rules/pga_classic/courses, nascar → "
        f"rules/nascar/tracks, mlb → rules/mlb_classic/parks; mma has none — create a stub marked "
        f"UNVERIFIED if the venue file is missing).\n\n"
        f"SOURCE-OF-TRUTH RULE: synthesize from BOTH the articles AND the vendor projections, "
        f"cross-checked against the framework and the OPEN lessons in lessons.yaml. BLEND the "
        f"qualitative article reads with the projection ownership/projections; cite each ownership "
        f"or projection number from its source (name the article OR the vendor). Where the vendors "
        f"disagree with each other, or a vendor disagrees with the articles, SURFACE that gap — it "
        f"is leverage signal (put it in Key themes / Leverage & fades).\n\n"
        f"HARD RULE — NEVER CREATE LINEUPS: write NO lineup tables, build NO rosters, and give NO "
        f"sample/example lineups or player groupings presented as a build. Name plays INDIVIDUALLY "
        f"only; this is a strategy doc the user hand-builds from — construction lives in the "
        f"separate sim tool, not here.\n\n"
        f"LEVERAGE COVERAGE — MANDATORY: if the bundle has a `## Leverage candidates to address` "
        f"section, EVERY player listed there must be ADDRESSED in `## Leverage & fades` or "
        f"`## Edges & tensions` with a one-line synthesis of their leverage/ceiling case (no play/fade "
        f"command needed — just surface them). A sub-10% high-ceiling play left "
        f"unmentioned is a coverage leak (the play that decides the slate from nowhere) — never "
        f"silently omit one.\n\n"
        f"MANDATORY pre-flight — do ALL of this SILENTLY as prep. **Do NOT print a checklist or a "
        f"pre-flight section; the user does not want to see it.** Only the RESULT of this prep shows, "
        f"inside the sections below. Confirm the article files are for the CURRENT slate (compare the "
        f"bundle's generation date + article file dates against today); if they look stale, do NOT "
        f"analyze a prior slate — instead open the doc with a single bold `⚠️` warning line and stop. "
        f"Read EVERY `articles/{slug}/` file (never silently skip one). Read the venue file. Read "
        f"`rules/{slug}/lessons.yaml` — apply every open lesson (hypothesis/validated) in the decisions "
        f"where it fits, and silently drop the ones whose mechanism doesn't. Run the framework's "
        f"pre-lock checks including Anchor-Equivalence (surfaced as a tension in `## Edges & tensions`). "
        f"If the bundle has a `## Process trend` section, read the SEQUENCES: a recurring weakness "
        f"(leverage capture repeatedly 0%, bust exposure climbing, violated fade calls, the same "
        f"shark-gap axis) MUST shape the relevant section below — e.g. weak leverage capture makes the "
        f"low-owned-definers screen the slate's priority. One bad slate is variance; a repeated "
        f"pattern is process signal.\n\n"
        f"Write a **SYNTHESIS-FIRST, tight, scannable** GPP slate brief to `{out_path}`. **This tool "
        f"ORGANIZES and SYNTHESIZES the data — it does NOT tell the user who to play.** Surface the "
        f"edges, tensions, mispricings, and rankings; the user makes every play/fade/build decision "
        f"themselves and builds in SaberSim. NO imperative play/fade commands, no roster shaping — "
        f"state what the data says and stop. A tight scannable brief, NOT an essay — read in 60 "
        f"seconds.\n\n"
        f"HARD WRITING RULES (apply to EVERY section):\n"
        f"- **Brevity:** every bullet ≤ ~25 words, ONE idea per line, no multi-sentence prose blocks. "
        f"Bold the player/decision. Cut anything that isn't a decision or its direct support.\n"
        f"- **Cite everything:** every play / leverage / fade names a SPECIFIC article line OR a "
        f"projection number (own %, ceiling, proj). NO framework-only justification with no "
        f"slate-specific data — if you can't cite it, cut it.\n"
        f"- **Readable:** use short tables where they compress; consistent, skimmable structure.\n\n"
        f"Sections, in THIS order (NO pre-flight/checklist section — that prep is silent):\n"
        f"1. `## Slate at a glance` — ≤6 lines: games/fights/races, implied totals or win probs, "
        f"weather, contests + field sizes. A short table, nothing more.\n"
        f"2. `## Edges & tensions` — THE STAR, right up top: the 3–6 things that actually matter this "
        f"slate, SYNTHESIZED — **NOT play/fade calls.** Each is ONE line: **the edge/tension** · the "
        f"cited data that reveals it (article line or number). Surface things like: where the "
        f"scoring/leverage concentrates, an ownership-vs-ceiling mispricing, where the vendors or "
        f"articles DISAGREE, a chalk cluster that's substitutable. **Anchor-Equivalence MUST appear "
        f"here** — but as a SURFACED observation (e.g. 'X and Y are near-identical profiles at "
        f"similar ownership'), NEVER as 'run the alternative.' If the bundle has a `## Field "
        f"tendencies` section, you MUST surface EVERY reliably-crowded cluster it lists here as a tension (mandatory address, not optional: a listed crowd left unsurfaced is a coverage leak) — 'the field piles into X/Y in your "
        f"<type> contests (in 3 of 4) — that's where leverage-away lives,' citing the exact in-N-of-M counts. Use NO "
        f"imperative verbs (no PLAY / FADE / run / cap / pair / build): state the edge and stop — the "
        f"user decides what to do with it. This is the synthesis the user reads first.\n"
        f"3. `## Top plays` — tiered **Core / Good / Okay** (same vocabulary as the Player pool; "
        f"Fades live in section 4, not here), one line each: **player** ($sal, own% per source) — "
        f"tier — ≤12-word cited why; append `· Leverage` to any low-owned high-ceiling play. No "
        f"paragraphs.\n"
        f"4. `## Leverage & fades` — two tight parts:\n"
        f"   - **Low-owned definers (MANDATORY screen):** for EVERY game/fight/race on the slate, "
        f"name the single sub-10%-owned high-ceiling play — INCLUDING ones the articles never named "
        f"— with its one-line ceiling path. This is the non-negotiable fix for the recurring miss "
        f"(the winning sub-10% definer that gets faded or never screened). Every spot gets a line.\n"
        f"   - **Fades:** a `**Fades:**` sub-header, then the chalk worth fading, each with the world "
        f"it needs (a fade is a bet). Name the player + verdict (FADE / LEAN FADE / UNDERWEIGHT).\n"
        f"5. `## Key themes` — ≤3 bullets: the structural storylines + where the sources DISAGREE "
        f"(article vs article / vendor vs vendor / article vs projection — that gap is the edge).\n"
        f"6. `## How to approach the slate` — 3–4 lines only. **This tool is focused on small-field "
        f"GPPs — Single Entry, 3-Max, and 5-Max ONLY** (no 150-max MME). Frame the winning shape for "
        f"a TIGHT all-unique set of 1/3/5 bullets: still ceiling + leverage over median (GPP), but "
        f"every one of your few lineups is a DISTINCT thesis — so leverage/anchor decisions must be "
        f"spread across your 1–5 lineups, not sprayed. Give the chalk-vs-contrarian lean and the "
        f"sharp-envelope target (≥1 sub-5% piece in most bullets, an elite anchor with downstream "
        f"differentiation, all-unique). **If the bundle has a `## Shark reality` section, anchor the "
        f"sharp-envelope target to ITS observed numbers** (own/slot, leverage%, anchor-exposure from "
        f"the pros who actually played YOUR contests) and name the gap to close — not just the static "
        f"playbook. If that section lists NAMED pros, cite the most relevant archetype as coaching — "
        f"e.g. 'moklovin (beat you 2/3) rides the chalk anchors and skips leverage — your edge vs him "
        f"is the sub-5% piece he never carries.' Descriptive only; surface it as the target and issue "
        f"no play/fade command. No restatement of the plays above.\n\n"
        f"Do not ask any questions — read the inputs and produce the file."
    )
    return _run_claude(prompt, out_path)


def run_grade(slug: str, contest_label: str, sport: str, lineups_text: str) -> dict:
    """Thesis check for HAND-BUILT lineups (the Grade tab's claude pass, on top of
    the deterministic checks in src/grader.py). For each pasted lineup: a one-line
    'how it wins' thesis grounded in the slate data — or THESIS-LESS — plus a
    portfolio distinctness read. GRADES ONLY: never builds, swaps, or fixes.

    Writes data/grade/<slug>.md. Returns {ok, error, duration_s, cost_usd}."""
    out_path = _REPO_ROOT / "data" / "grade" / f"{slug}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = (
        f"You are grading the user's HAND-BUILT {contest_label} DK lineups (sport: {sport}) "
        f"before lock. HARD RULE: you grade — you NEVER build, select, swap, fix, or suggest "
        f"replacement players/lineups. Name weaknesses; the user decides.\n\n"
        f"Read: the slate strategy at `data/slate_analysis/{slug}.md`, the player pool at "
        f"`data/player_pool/{slug}.md`, and `rules/{slug}/lessons.yaml` (open lessons only).\n\n"
        f"The lineups (one per line):\n{lineups_text}\n\n"
        f"Write `{out_path}` with:\n"
        f"1. `## Thesis check` — for EACH lineup, ONE line: **Lineup N** — its 'how it wins' "
        f"thesis in one sentence, citing a specific data point (article read, own%, ceiling), "
        f"OR `**THESIS-LESS**` if no coherent winning story exists. Every lineup needs an "
        f"articulable thesis — vague labels don't count.\n"
        f"2. `## Distinctness` — do the lineups answer DIFFERENT what-ifs? Name any pair that "
        f"answers the same question (competing lineups).\n"
        f"3. `## Lessons that activate` — any open lesson from lessons.yaml this set of "
        f"lineups triggers (state the lesson id + mechanism), or 'None.'\n"
        f"≤25 words per bullet. NO play/fade commands, NO alternative lineups, NO swap "
        f"suggestions. Do not ask questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_player_pool(slug: str, contest_label: str, sport: str) -> dict:
    """Build the ranked, annotated player pool: every rosterable player from the
    loaded projections minus the strategy's fades, ranked for GPP with a short
    write-up each. Membership is computed deterministically here; Claude only
    ranks + writes up, grounded in the articles + slate strategy.

    Writes data/player_pool/<slug>.md. Returns {ok, error, duration_s, cost_usd}.
    """
    from src import sessions
    from src.slate_analysis import load_persisted
    from src.player_pool import build_pool, extract_fades, apply_fades

    sources = sessions.load_sources(slug)
    if not sources:
        return {"ok": False, "error": "No projections loaded — upload vendor CSVs in the "
                "Projections tab first.", "duration_s": 0.0, "cost_usd": None}
    # Fades come from the slate strategy WHEN one exists; without it, rank the full
    # pool so a ranking can be pulled standalone (e.g. a no-prep week / quick board).
    persisted = load_persisted(slug)
    full = build_pool(sources)
    if persisted:
        kept, removed = apply_fades(full, extract_fades(persisted["markdown"]))
        strategy_note = ("Also read the written slate strategy at "
                         f"`data/slate_analysis/{slug}.md`.")
    else:
        kept, removed = full, []
        strategy_note = ("No slate strategy was generated for this slate — rank the FULL "
                         "pool below (no fades removed); ground the ranking in the articles "
                         "+ framework.")
    if full.empty:
        return {"ok": False, "error": "Player pool is empty — check the loaded projections.",
                "duration_s": 0.0, "cost_usd": None}
    is_mma = sport == "mma"

    # The exact playable set, as a fixed table Claude must rank without adding/dropping.
    def _row(r):
        own = f"{r['ownership']:.0f}%" if r.get("ownership") is not None else "n/a"
        proj = f"{r['proj_points']:.1f}" if r.get("proj_points") is not None else "n/a"
        sal = f"${int(r['salary']):,}" if r.get("salary") is not None else "n/a"
        opp = f" vs {r['opponent']}" if r.get("opponent") else ""
        extra = ""
        if is_mma:
            ceil = f"{r['ceiling']:.1f}" if r.get("ceiling") is not None else "n/a"
            wp = f"{r['win_prob'] * 100:.0f}%" if r.get("win_prob") is not None else "n/a"
            extra = f", ceiling(win) {ceil}, win% {wp}"
        return f"- {r['name']} — {sal}, proj own {own}, proj pts {proj}{extra}{opp}"

    player_lines = "\n".join(_row(r) for _, r in full.iterrows())
    removed_note = (", ".join(removed)) if removed else "none"
    out_path = _REPO_ROOT / "data" / "player_pool" / f"{slug}.md"
    bundle_path = build_bundle(slug, contest_label, sport)

    prompt = (
        f"Write the {contest_label} PLAYER POOL — a ranked, annotated board of the rosterable "
        f"players, for a GPP hand-builder. **This board IS what the user builds lineups from** — the "
        f"top tiers (Core/Good/Okay) are the build set, the Fade tier is what to avoid. Player "
        f"analysis + ranking is the priority; make every write-up a sharp, buildable read.\n\n"
        f"The pool membership is FIXED — these {len(full)} players, and ONLY these. Do NOT add, "
        f"drop, or rename any player. The strategy DESIGNATES these as fades — you MUST give each of "
        f"them the `Fade` tier (they STAY on the board, ranked at the bottom): {removed_note}.\n"
        f"{player_lines}\n\n"
        f"Read for grounding: the bundle at `{bundle_path}` and — this is MANDATORY — EVERY single "
        f"slate-data file it lists under `articles/{slug}/`. Read ALL of them, no exceptions: article "
        f"PDFs, notes (.txt/.md), data CSVs (read as text tables), AND every photo/screenshot/image "
        f"(.png/.jpg/.jpeg — use the Read tool, it reads images visually). Do not skip a file because "
        f"it looks redundant. {strategy_note} "
        f"Also read the strategy docs `rules/{slug}/philosophy.md` + `rules/{slug}/framework.md`.\n\n"
        f"SOURCE-OF-TRUTH RULE: the ranking and every write-up come from those documents. "
        f"Cite ownership AS THE ARTICLES STATE IT (the projected own above is a "
        f"reference, not the source of truth). GPP-framed throughout (ceiling/leverage, not floor).\n\n"
        f"Rank ALL {len(full)} players 1..N by GPP play-priority for this slate (best play = 1). "
        f"Write `{out_path}` as:\n"
        f"- A one-line header `# {contest_label} — Player pool` and a one-sentence note that this is "
        f"a synthesized, ranked reference (the user decides who to play).\n"
        f"- FIRST, an easy-to-read **ranked Markdown table** — the whole board at a glance, best "
        f"to worst, one row per player. **Lead with the DATA; the tier is the LAST column (a summary "
        f"read, not the headline).** Columns EXACTLY: "
        + ("`| Rank | Fighter | Sal | Proj | Ceiling | Win% | Own | How it wins | Tier |`, where "
           "Ceiling = the ceiling(win) value and Win% = the win% shown per player above, "
           "'How it wins' is ≤8 words, and Tier carries any `· Leverage` label.\n"
           if is_mma else
           "`| Rank | Player | Sal | Proj | Own | How it wins | Tier |`, where 'How it wins' is "
           "≤8 words and Tier carries any `· Leverage` label.\n") +
        f"- THEN a single continuous numbered list (the detailed write-ups), best to worst. "
        f"Each entry LEADS WITH THE DATA, tier LAST as a one-word read:\n"
        f"  `**N. Player Name** — $salary, own% (per source), proj X[, ceiling Y]` then a 1–2 "
        f"sentence synthesis: HOW IT WINS (the ceiling path / the edge) + the key risk or condition, "
        f"and END the line with `— <tier>` (+ `· Leverage` if it applies). Tight and slate-specific "
        f"— no filler, no play/fade command.\n"
        f"- **Tier vocabulary (ALL sports) — exactly one of `Core`, `Good`, `Okay`, `Fade`** "
        f"(best→worst): **Core** = build around it, an anchor of your lineups; **Good** = strong, "
        f"plays in many of your builds; **Okay** = usable pivot/filler; **Fade** = avoid (this "
        f"INCLUDES every strategy-designated fade named above, plus anything else your read says to "
        f"avoid).\n"
        f"- **Leverage label:** if a play is a LEVERAGE play (low-owned + high-ceiling — the "
        f"sub-owned play that can break the slate), append `· Leverage` to its tier "
        f"(e.g. `Core · Leverage`, `Good · Leverage`, `Okay · Leverage`). Leverage is ORTHOGONAL to "
        f"quality (any tier except Fade can carry it) and MUST be labeled wherever it applies — a "
        f"leverage play left unlabeled is a miss. Use the SAME tier string (incl. any `· Leverage`) "
        f"in both the table Tier column and the list entry.\n"
        f"- **Field-crowds flag (mandatory):** if the bundle at `{bundle_path}` has a `## Field "
        f"tendencies` section, you MUST append a small `(field crowds)` note in the write-up of "
        f"EVERY board player that appears in its reliably-crowded list — no exceptions. It is a "
        f"heads-up that the field piles in, not a fade command.\n"
        f"- Then a `## Leverage candidates addressed` section: if the bundle at `{bundle_path}` "
        f"lists a `## Leverage candidates to address` section, confirm EACH player there is ranked "
        f"above (name it + its rank) — carrying the `· Leverage` label unless you tiered it `Fade` "
        f"(then give the one-line reason). Never leave a sub-10% high-ceiling candidate unaddressed "
        f"— that is the coverage leak this guard exists to catch.\n"
        f"- End the file with a `## Sources read` section: state how many `articles/{slug}/` "
        f"slate-data files you read (e.g. 'All 4 files read'), and EXPLICITLY LIST any file you "
        f"could NOT read or parse, with the reason (e.g. a PDF that wouldn't extract). If every file "
        f"parsed, say so. This is mandatory — coverage must be visible.\n\n"
        f"Every one of the {len(full)} players gets exactly one ranked entry.\n\n"
        f"HARD RULE — NEVER CREATE LINEUPS: this is a board of INDIVIDUAL players ranked "
        f"independently. Do NOT assemble, suggest, or imply any lineup, roster, or combination "
        f"of players — no N-man builds, no 'play these together', no sample/example lineups, no "
        f"stacks or pairings presented as a build. Each entry stands alone; construction lives in "
        f"the separate sim tool, not here.\n\n"
        f"Do not ask any questions — read the inputs and produce the file."
    )
    return _run_claude(prompt, out_path)


def run_autopsy_review(slug: str, contest_label: str, sport: str) -> dict:
    """Post-autopsy learning run: grade the archived slate's process, update
    the lesson ledger + venue file, and write proposed (not applied)
    framework changes to <history_dir>/autopsy_review.md."""
    from src.history import latest_history_dir

    hist_dir = latest_history_dir(slug)
    if hist_dir is None:
        return {"ok": False, "error": "No archived slate found — log an autopsy first.",
                "duration_s": 0.0, "cost_usd": None}

    out_path = hist_dir / "autopsy_review.md"
    prompt = (
        f"Run the post-autopsy review for the archived {contest_label} slate at `{hist_dir}`. "
        f"Read its manifest.json, slate_analysis.md, autopsy.json, and results.json, "
        f"the shark head-to-head at `{hist_dir}/shark_gap.json` (structural you-vs-the-pros), "
        f"the own-strategy adherence grade at `{hist_dir}/adherence.json` (if present), "
        f"the player-pool tier calibration at `{hist_dir}/pool_calibration.json` (if present — "
        f"did the board's tiers hold up, and who got buried?), "
        f"the last few rows of `rules/{slug}/results.jsonl` (the process TREND — leverage capture, "
        f"bust exposure, adherence across slates, not just this one), "
        f"the latest entries in `rules/{slug}/autopsy_data.jsonl`, "
        f"and the lesson ledger at "
        f"`rules/{slug}/lessons.yaml` (create it with the standard header from CLAUDE.md's "
        f"'Lesson ledger' section if missing). Then, following the 'Post-autopsy ritual' in CLAUDE.md:\n"
        f"1. GRADE THE PROCESS: judged by the strategy's substance (there is no printed checklist), "
        f"were the pre-flight checks honored — venue file, open lessons, Anchor-Equivalence? "
        f"Which open lessons were applied vs ignored, and did ignored ones cost anything? Did the "
        f"slate strategy's synthesized edges/tensions, tiers, and Top plays hold up against the DK "
        f"actuals in autopsy.json (slate-defining low-owned plays, your entries vs the winners)?\n"
        f"1b. SHARK GAP: from `shark_gap.json`, name the structural axis where the tracked pros most "
        f"separated from you (own/slot, leverage %, chalk-anchor exposure, uniqueness). If the SAME "
        f"axis has separated before (check prior autopsy_data.jsonl / lessons), that is a RECURRING "
        f"structural leak — the sharpest kind of process lesson. State the mechanism ('I under-own the "
        f"field's chalk anchors the pros ride', etc.), not the result.\n"
        f"1c. ADHERENCE: from `adherence.json` (when present), grade DISCIPLINE separately from "
        f"analysis: did the entered lineups honor the strategy's own fade/under-own calls, and did "
        f"any lineup carry the named leverage candidates? A violated own-call is a process finding "
        f"even when it happened to score well (results don't launder discipline). If the results.jsonl "
        f"trend shows the same violation pattern across slates, birth/confirm a mechanism lesson.\n"
        f"1d. CODIFIED-RULE CHECK: for each lesson in `rules/{slug}/lessons.yaml` with status "
        f"'codified', note whether the archived strategy actually APPLIED it (or it didn't trigger "
        f"this slate) and whether its MECHANISM held against the DK actuals. Codification is not "
        f"tenure: a codified rule whose mechanism has now failed in 2+ slates gets a demotion "
        f"proposal in '## Proposed codifications' (retire or narrow its scope), with the exact "
        f"framework.md edit. Same GPP guard — a lost contest alone is not a mechanism failure.\n"
        f"2. UPDATE `rules/{slug}/lessons.yaml` directly (Edit tool): add confirmations/contradictions "
        f"with this slate's date and history dir; promote status to 'validated' where confirmations "
        f"exist; add new 'hypothesis' lessons born from this autopsy — mechanism-based, not "
        f"result-based. A recurring shark-gap axis (1b) should birth or confirm a mechanism lesson.\n"
        f"3. UPDATE THE VENUE FILE for this slate's venue (sport `{sport}`; see CLAUDE.md for the "
        f"venue dir; create the file from the archived strategy if missing): append a date-stamped "
        f"'Per-slate observation' line with what this slate proved or disproved about the venue.\n"
        f"4. WRITE `{out_path}` with sections: '## Process scorecard', '## Lesson ledger changes', "
        f"'## Venue file changes', and '## Proposed codifications' — for any lesson meeting the "
        f"promotion criteria (3 confirming slates) write the exact framework.md/philosophy.md edit "
        f"you propose; for retirement candidates (2 mechanism contradictions) the same. If nothing "
        f"qualifies, write 'None this slate.' under that heading. "
        f"Do NOT edit framework.md or philosophy.md in this run — proposals only; the user approves.\n"
        f"GPP guard: a bad ROI or a lost contest is NEVER a contradiction by itself; only mechanism "
        f"failures count. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_apply_proposals(slug: str) -> dict:
    """Apply the user-approved '## Proposed codifications' from the latest
    autopsy review to framework.md/philosophy.md + the lesson ledger."""
    from src.history import latest_history_dir

    hist_dir = latest_history_dir(slug)
    review_path = hist_dir / "autopsy_review.md" if hist_dir else None
    if review_path is None or not review_path.exists():
        return {"ok": False, "error": "No autopsy review found — run the review first.",
                "duration_s": 0.0, "cost_usd": None}

    prompt = (
        f"Read `{review_path}`, section '## Proposed codifications'. The user has APPROVED these "
        f"proposals. Apply each proposed edit to `rules/{slug}/framework.md` / "
        f"`rules/{slug}/philosophy.md` exactly as written, then update `rules/{slug}/lessons.yaml`: "
        f"set the affected lessons' status to 'codified' (with codified_in naming the doc + section) "
        f"or 'retired' (with retired_reason). Finally append a line "
        f"'## Applied' with the current changes summarized to the end of `{review_path}`. "
        f"Do not ask any questions."
    )
    return _run_claude(prompt, review_path)


def _sim_table(df, cols, n: int = 15) -> str:
    """Plain pipe-table text of a df's first n rows for embedding in a prompt."""
    if df is None or getattr(df, "empty", True):
        return "(none)"
    cols = [c for c in cols if c in df.columns]
    if not cols:
        return "(none)"
    lines = [" | ".join(cols)]
    for _, r in df.head(n).iterrows():
        lines.append(" | ".join("" if r[c] is None else str(r[c]) for c in cols))
    return "\n".join(lines)


def run_ledger_review(slug: str) -> dict:
    """Lesson-ledger hygiene review: turn the deterministic flags (stale, near-/
    overdue-promotion, merge candidates) into reasoned PROPOSALS at
    rules/<slug>/ledger_review.md. Edits nothing in the ledger — proposals only."""
    from src import ledger_hygiene

    lessons_path = _REPO_ROOT / "rules" / slug / "lessons.yaml"
    if not lessons_path.exists():
        return {"ok": False, "error": "No lessons.yaml for this sport yet.",
                "duration_s": 0.0, "cost_usd": None}

    report_md = ledger_hygiene.report_md(ledger_hygiene.hygiene_report(slug))
    out_path = _REPO_ROOT / "rules" / slug / "ledger_review.md"
    prompt = (
        f"Review the lesson ledger at `{lessons_path}` for HYGIENE. A deterministic pre-pass already "
        f"flagged candidates (below) — turn them into reasoned PROPOSALS; do NOT apply anything. "
        f"Read `{lessons_path}` in full first.\n\n"
        f"Deterministic flags:\n{report_md}\n\n"
        f"Write `{out_path}` with these sections:\n"
        f"1. `## Retire candidates` — for each flagged stale hypothesis, decide RETIRE or KEEP with a "
        f"one-line MECHANISM reason. GPP guard: a lesson untested only because no RELEVANT slate "
        f"occurred (e.g. a showdown lesson with no showdown slate since `born`) is KEEP, not retire. "
        f"Name the retired_reason to write if retiring.\n"
        f"2. `## Near-promotion` — for each lesson at 2 of 3 confirming slates, name the exact "
        f"mechanism a third slate must confirm to promote, so the next autopsy knows what to watch.\n"
        f"3. `## Overdue promotion` — for any lesson already at ≥3 confirming slates but not codified, "
        f"propose the exact framework.md / philosophy.md edit to codify it.\n"
        f"4. `## Merge candidates` — for each flagged pair, decide MERGE or KEEP-SEPARATE with a "
        f"reason; if merge, name which id survives and give the combined statement.\n\n"
        f"Every change is a PROPOSAL — do NOT edit lessons.yaml, framework.md, or philosophy.md in "
        f"this run; the user approves in the app. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_apply_ledger_proposals(slug: str) -> dict:
    """Apply the user-approved ledger_review.md to lessons.yaml (+ framework/
    philosophy for any approved codifications)."""
    review_path = _REPO_ROOT / "rules" / slug / "ledger_review.md"
    if not review_path.exists():
        return {"ok": False, "error": "No ledger review found — run the review first.",
                "duration_s": 0.0, "cost_usd": None}

    prompt = (
        f"Read `{review_path}`. The user has APPROVED these ledger-hygiene proposals. Apply them to "
        f"`rules/{slug}/lessons.yaml`: set RETIRE-decided lessons' status to 'retired' with the "
        f"retired_reason; MERGE each pair marked merge (keep the surviving id with the combined "
        f"statement, set the other to 'retired' with retired_reason 'merged into <id>'); for approved "
        f"codifications apply the exact `rules/{slug}/framework.md` / `rules/{slug}/philosophy.md` "
        f"edit and set the lesson status to 'codified' with codified_in naming the doc + section. "
        f"Leave every KEEP / KEEP-SEPARATE lesson untouched. Append a '## Applied' summary line to "
        f"`{review_path}`. Do not ask any questions."
    )
    return _run_claude(prompt, review_path)
