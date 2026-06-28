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

    # Snapshot the prior file mtime so we can confirm a fresh write below.
    prior_mtime = out_path.stat().st_mtime if out_path.exists() else None

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
        f"section, EVERY player listed there must appear in `## Leverage & fades` or `## Decisions` "
        f"as an explicit PLAY or PASS with a one-line mechanism. A sub-10% high-ceiling play left "
        f"unmentioned is a coverage leak (the play that decides the slate from nowhere) — never "
        f"silently omit one.\n\n"
        f"MANDATORY pre-flight: confirm the article files are for the CURRENT slate (compare the "
        f"bundle's generation date + the article file dates against today; if they look stale, SAY "
        f"SO in the checklist instead of analyzing a prior slate). In the checklist, state how many "
        f"`articles/{slug}/` files you read and EXPLICITLY LIST any file you could NOT read or parse "
        f"(with the reason) — coverage must be visible, never silently skip a file. Read the venue file. Read "
        f"`rules/{slug}/lessons.yaml` — every open lesson (hypothesis/validated) must be applied "
        f"(name where) or rejected (name the mechanism reason). Run the framework's pre-lock checks "
        f"including Anchor-Equivalence.\n\n"
        f"Write a concise, scannable, GPP-framed slate strategy to `{out_path}` with EXACTLY these "
        f"sections, in order:\n"
        f"1. `## Pre-flight checklist` — slate confirmed (article dates), venue file "
        f"read, open lessons applied-or-rejected, framework pre-lock checks (incl. Anchor-Equivalence), "
        f"prior autopsy notes scanned, sharp envelope noted as the target. Each line checked `[x]` "
        f"with specifics or `[ ]` with the reason. No checklist, no valid output.\n"
        f"2. `## Slate at a glance` — brief facts table from the articles (games/fights/races, "
        f"implied totals or win probs, weather, contests + field sizes). Keep it short.\n"
        f"3. `## Top plays` — tiered (e.g. core / pivots / darts). Each play: the cited ownership "
        f"(name the source — article or vendor projection) + a one-line WHY. The plays the articles "
        f"AND projections surface, weighted by your read.\n"
        f"4. `## How to approach the slate` — the plain-English game plan for a hand-builder: what "
        f"the winning shape looks like, how chalk-vs-contrarian to lean (field-size aware), the "
        f"sharp-envelope target (≥1 sub-5% leverage piece, ceiling over median, all-unique lineups).\n"
        f"5. `## Key themes` — the structural storylines, INCLUDING where the sources DISAGREE — "
        f"article vs article, vendor vs vendor, or article vs projection — that disagreement is the "
        f"edge; name both sides and which you trust and why.\n"
        f"6. `## Leverage & fades` — the underowned plays worth the leverage and the chalk worth "
        f"fading, each with the mechanism (a fade is a bet — price the world it needs).\n"
        f"7. `## Decisions` — 2–5 PLAY/PASS/MIX calls, in priority order, each with a one-sentence "
        f"mechanism. The Anchor-Equivalence call MUST appear here as one of the decisions.\n\n"
        f"Do not ask any questions — read the inputs and produce the file."
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
    persisted = load_persisted(slug)
    if not persisted:
        return {"ok": False, "error": "No slate strategy yet — generate it first so the fades "
                "are known.", "duration_s": 0.0, "cost_usd": None}

    full = build_pool(sources)
    kept, removed = apply_fades(full, extract_fades(persisted["markdown"]))
    if kept.empty:
        return {"ok": False, "error": "Player pool is empty after removing fades — check the "
                "loaded projections.", "duration_s": 0.0, "cost_usd": None}

    # The exact playable set, as a fixed table Claude must rank without adding/dropping.
    def _row(r):
        own = f"{r['ownership']:.0f}%" if r.get("ownership") is not None else "n/a"
        proj = f"{r['proj_points']:.1f}" if r.get("proj_points") is not None else "n/a"
        sal = f"${int(r['salary']):,}" if r.get("salary") is not None else "n/a"
        opp = f" vs {r['opponent']}" if r.get("opponent") else ""
        return f"- {r['name']} — {sal}, proj own {own}, proj pts {proj}{opp}"

    player_lines = "\n".join(_row(r) for _, r in kept.iterrows())
    removed_note = (", ".join(removed)) if removed else "none"
    out_path = _REPO_ROOT / "data" / "player_pool" / f"{slug}.md"
    bundle_path = build_bundle(slug, contest_label, sport)

    prompt = (
        f"Write the {contest_label} PLAYER POOL — a ranked, annotated board of the rosterable "
        f"players, for a GPP hand-builder.\n\n"
        f"The pool membership is FIXED — these {len(kept)} players, and ONLY these. Fades are "
        f"already removed (excluded: {removed_note}). Do NOT add, drop, or rename any player:\n"
        f"{player_lines}\n\n"
        f"Read for grounding: the bundle at `{bundle_path}` and — this is MANDATORY — EVERY single "
        f"slate-data file it lists under `articles/{slug}/`. Read ALL of them, no exceptions: article "
        f"PDFs, notes (.txt/.md), data CSVs (read as text tables), AND every photo/screenshot/image "
        f"(.png/.jpg/.jpeg — use the Read tool, it reads images visually). Do not skip a file because "
        f"it looks redundant. Also read the written slate strategy at `data/slate_analysis/{slug}.md` "
        f"and the strategy docs `rules/{slug}/philosophy.md` + `rules/{slug}/framework.md`.\n\n"
        f"SOURCE-OF-TRUTH RULE: the ranking and every write-up come from those documents + the "
        f"slate strategy. Cite ownership AS THE ARTICLES STATE IT (the projected own above is a "
        f"reference, not the source of truth). GPP-framed throughout (ceiling/leverage, not floor).\n\n"
        f"Rank ALL {len(kept)} players 1..N by GPP play-priority for this slate (best play = 1). "
        f"Write `{out_path}` as:\n"
        f"- A one-line header `# {contest_label} — Player pool` and a one-sentence note that fades "
        f"are removed and this is a hand-build reference.\n"
        f"- Then a single continuous numbered list, best to worst. Each entry on its own line:\n"
        f"  `**N. Player Name** ($salary, own% per source) — *tier* —` then a 1–2 sentence write-up: "
        f"the role (Core / Pivot / Dart), HOW IT WINS (the ceiling path / the edge), and the key "
        f"risk or condition. Keep each write-up tight and specific to this slate — no filler.\n"
        f"- Tier tag must be one of Core, Pivot, or Dart based on your read.\n"
        f"- Then a `## Leverage candidates addressed` section: if the bundle at `{bundle_path}` "
        f"lists a `## Leverage candidates to address` section, confirm EACH player there is either "
        f"ranked above (name it + its rank) or was faded out of the pool (name it + the one-line "
        f"reason). Never silently drop a sub-10% high-ceiling candidate — that is the coverage leak "
        f"this guard exists to catch.\n"
        f"- End the file with a `## Sources read` section: state how many `articles/{slug}/` "
        f"slate-data files you read (e.g. 'All 4 files read'), and EXPLICITLY LIST any file you "
        f"could NOT read or parse, with the reason (e.g. a PDF that wouldn't extract). If every file "
        f"parsed, say so. This is mandatory — coverage must be visible.\n\n"
        f"Every one of the {len(kept)} players gets exactly one ranked entry.\n\n"
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
        f"the latest entries in `rules/{slug}/autopsy_data.jsonl`, "
        f"and the lesson ledger at "
        f"`rules/{slug}/lessons.yaml` (create it with the standard header from CLAUDE.md's "
        f"'Lesson ledger' section if missing). Then, following the 'Post-autopsy ritual' in CLAUDE.md:\n"
        f"1. GRADE THE PROCESS: was the pre-flight checklist present and honest in slate_analysis.md? "
        f"Which open lessons were applied vs ignored, and did ignored ones cost anything? Did the "
        f"slate strategy's PLAY/PASS/MIX decisions and Top plays hold up against the DK actuals in "
        f"autopsy.json (slate-defining low-owned plays, your entries vs the winners)?\n"
        f"2. UPDATE `rules/{slug}/lessons.yaml` directly (Edit tool): add confirmations/contradictions "
        f"with this slate's date and history dir; promote status to 'validated' where confirmations "
        f"exist; add new 'hypothesis' lessons born from this autopsy — mechanism-based, not "
        f"result-based.\n"
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


def run_sim_review(slug: str, contest_label: str, sport: str) -> dict:
    """Write a 'what the sim says' summary from the uploaded SaberSim pool to
    data/sim_analysis/<slug>.md. ANALYTICS ONLY — individual plays + combos to
    fade, never an assembled lineup."""
    from src import sim_data, sim_sessions, dk_ids, player_pool
    from src import sessions as _sess

    pool_p = sim_sessions.pool_path(slug)
    if pool_p is None:
        return {"ok": False, "error": "No sim pool uploaded — add a SaberSim export in the Sim Data tab first.",
                "duration_s": 0.0, "cost_usd": None}
    pool = sim_data.load_sim_pool(str(pool_p))
    if pool.get("n", 0) == 0:
        return {"ok": False, "error": "Couldn't parse the sim pool CSV.",
                "duration_s": 0.0, "cost_usd": None}

    dkmap_p = sim_sessions.dkmap_path(slug)
    uploaded_map = dk_ids.parse_id_to_name(str(dkmap_p)) if dkmap_p else None
    id_to_name = dk_ids.resolve_id_to_name(slug, uploaded_map)
    proj = player_pool.build_pool(_sess.load_sources(slug))
    exp = sim_data.player_exposure(pool, id_to_name, proj if not proj.empty else None)
    gb = sim_data.good_bad_plays(exp)
    combos = sim_data.chalky_combinations(pool, id_to_name)

    out_path = _REPO_ROOT / "data" / "sim_analysis" / f"{slug}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tables = (
        f"SIM CORE (highest exposure):\n{_sim_table(gb.get('good'), ['player','sim_exposure_pct','field_own_pct','avg_saber'])}\n\n"
        f"SIM FADES (lowest exposure):\n{_sim_table(gb.get('bad'), ['player','sim_exposure_pct','field_own_pct'])}\n\n"
        f"LEVERAGE (sim >> field own):\n{_sim_table(gb.get('leverage'), ['player','sim_exposure_pct','field_own_pct','edge'])}\n\n"
        f"TRAPS (field own >> sim):\n{_sim_table(gb.get('trap'), ['player','sim_exposure_pct','field_own_pct','edge'])}\n\n"
        f"CHALKY COMBINATIONS (joint exposure across {pool['n']} sim lineups):\n{_sim_table(combos, ['size','combo','joint_exposure_pct'])}\n"
    )
    prompt = (
        f"Write a concise GPP read of what SaberSim says for the {contest_label} slate, to "
        f"`{out_path}`. The deterministic sim tables are below (computed from {pool['n']} sim "
        f"lineups). Also read the written slate strategy at `data/slate_analysis/{slug}.md` if it "
        f"exists, to compare the sim's read against the strategy.\n\n"
        f"{tables}\n"
        f"Write these sections:\n"
        f"1. `## Sim core` — the plays SaberSim is heaviest on (name each + its sim exposure; note "
        f"where field ownership is much lower = the sim likes a play the field sleeps on).\n"
        f"2. `## Sim fades` — notable players the sim avoids (low/zero exposure), especially any the "
        f"field is high on (trap chalk).\n"
        f"3. `## Leverage the sim sees` — the biggest sim-exposure-over-field-ownership edges.\n"
        f"4. `## Chalky combinations to be aware of` — the most over-represented player pairs/trios "
        f"in the sim pool; frame them as DUPLICATION RISK to fade or differentiate from, never as "
        f"combos to play together.\n"
        f"5. `## Sim vs the strategy` — one short paragraph: where the sim agrees/disagrees with the "
        f"slate strategy, and what that disagreement implies.\n\n"
        f"HARD RULE — NEVER BUILD LINEUPS: name INDIVIDUAL plays and player combinations only. Do "
        f"NOT assemble, suggest, rank, or imply any full lineup/roster — this is sim analytics the "
        f"user hand-builds from, not a builder. Do not ask any questions — produce the file."
    )
    return _run_claude(prompt, out_path)


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
