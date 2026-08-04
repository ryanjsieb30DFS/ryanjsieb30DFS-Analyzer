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


def _run_claude(prompt: str, out_path: Path, collateral: list | None = None) -> dict:
    """Run `claude -p` headlessly and confirm `out_path` was freshly written.

    `collateral` lists the OTHER files the prompt instructs claude to edit
    (lessons.yaml, framework.md, …). They are snapshotted before the run and
    restored on any failure — otherwise a timed-out review leaves half-edited
    ledgers behind while only out_path rolls back. A collateral *.yaml file is
    also parse-validated after a successful run; broken YAML restores
    everything and fails the run.

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
    # None value = the file didn't exist pre-run (restore = delete).
    _collateral = [Path(p) for p in (collateral or [])]
    _coll_bytes = {p: (p.read_bytes() if p.exists() else None) for p in _collateral}

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

    def _rollback_collateral():
        for p, b in _coll_bytes.items():
            try:
                if b is None:
                    if p.exists():
                        p.unlink()
                elif not p.exists() or p.read_bytes() != b:
                    p.write_bytes(b)
            except OSError:
                pass  # best-effort, same as _rollback_partial

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
        _rollback_collateral()
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
        _rollback_collateral()
        return {"ok": False, "error": msg, "duration_s": duration, "cost_usd": cost}

    # Confirm a fresh output file actually landed.
    if not out_path.exists() or out_path.stat().st_mtime == prior_mtime:
        _rollback_collateral()
        return {"ok": False,
                "error": "Claude ran but didn't write the output file. Check the inputs and try again.",
                "duration_s": duration, "cost_usd": cost}

    # A collateral YAML ledger (lessons.yaml) that no longer parses is worse
    # than a failed run — everything downstream (hygiene, reviews, promotions)
    # reads it. Restore the pre-run state and fail loudly.
    for p in _collateral:
        if p.suffix in (".yaml", ".yml") and p.exists():
            try:
                import yaml  # local import, matching ledger_hygiene
                yaml.safe_load(p.read_text())
            except Exception as ye:  # noqa: BLE001 — YAMLError or read error
                _rollback_partial()
                _rollback_collateral()
                return {"ok": False,
                        "error": f"Claude's edit broke {p.name} ({ye}). "
                                 f"All files were restored to their pre-run state.",
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
        f"rules/nascar/tracks; mma has none — create a stub marked "
        f"UNVERIFIED if the venue file is missing).\n\n"
        f"SOURCE-OF-TRUTH RULE: synthesize from BOTH the articles AND the vendor projections, "
        f"cross-checked against the framework and the OPEN lessons in lessons.yaml. BLEND the "
        f"qualitative article reads with the projection ownership/projections; cite each ownership "
        f"or projection number from its source (name the article OR the vendor). Where the vendors "
        f"disagree with each other, or a vendor disagrees with the articles, SURFACE that gap — it "
        f"is leverage signal (put it in Key themes / the Leverage section).\n\n"
        f"HARD RULE — NEVER CREATE LINEUPS: write NO lineup tables, build NO rosters, and give NO "
        f"sample/example lineups or player groupings presented as a build. Name plays INDIVIDUALLY "
        f"only; this is a strategy doc the user hand-builds from — construction lives in the "
        f"separate sim tool, not here.\n\n"
        f"LEVERAGE COVERAGE — MANDATORY: if the bundle has a `## Leverage candidates to address` "
        f"section, EVERY player listed there must be ADDRESSED in `## Leverage` or "
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
        f"themselves and builds in the Sim tool (sibling repo — SaberSim was cancelled "
        f"7/18/26). NO imperative play/fade commands, no roster shaping — "
        f"state what the data says and stop. Scannable structure, but every line fully understandable "
        f"on its own — clarity over compression, always.\n\n"
        f"HARD WRITING RULES (apply to EVERY section — user directive 7/27/26: 'spell it out like "
        f"it's for a 5th grader; more words is totally fine'):\n"
        f"- **Write for a 5th grader. This is the master rule.** Short sentences. Ordinary words. "
        f"One fact at a time. After you write each sentence, ask: would a smart 11-year-old have to "
        f"re-read this, or ask what a word means? If yes, REWRITE IT. More words is always fine — "
        f"confusion is not.\n"
        f"- **Say the plain meaning FIRST, put the DFS word in parentheses after.** Write 'the "
        f"players most teams will pick (the chalk)', NOT 'the chalk (the most-picked players)'. The "
        f"plain phrase carries the sentence; the DFS word tags along so the user learns it. Do this "
        f"EVERY time the idea appears, in every section — not just the first time. The user has said "
        f"the verbiage loses him; never assume a term stuck from an earlier section.\n"
        f"- **Open every section with one plain sentence saying what the section is for.** Example: "
        f"'This section shows where most of the crowd is putting their players.' The user should "
        f"always know why he is reading a section before the details start.\n"
        f"- **ONE IDEA PER SENTENCE. Aim for ~15 words, hard stop at 25.** Do NOT chain clauses with "
        f"semicolons, dashes or 'and'. Do NOT put more than TWO numbers in one sentence — split it. "
        f"Prefer four short sentences over one dense one. Length is fine; density is the enemy.\n"
        f"- **Explain what every number MEANS, not just what it is.** Not '34% owned' but '34% "
        f"owned — about 1 of every 3 teams will have him'. Not 'ceiling 110' but 'his best "
        f"realistic night is about 110 points (his ceiling)'. A number without its meaning is "
        f"jargon with digits.\n"
        f"- **NEVER print a bundle-internal file reference.** 'image-35', 'image-40' and similar are "
        f"filenames only you can see — the user cannot tell what they point at. Describe what the "
        f"thing IS instead: 'the Indy last-four-races chart', 'the practice-speed table'. A real "
        f"source NAME is fine and preferred ('Dustin's Deep Dive', 'the DFR rankings'), but spell "
        f"out an initialism the FIRST time it appears in the document, then the short form is fine.\n"
        f"- **The DFS terms that MUST always get the plain-first treatment:** ownership, chalk, "
        f"leverage, ceiling, floor, dupe/duplication, anchor, anchor-equivalence, fade, dominator, "
        f"place differential, fish trap, own-per-slot, stars-and-scrubs, punt, and every vendor term "
        f"(coffin, dock, boost, sim-optimal, steam, exposure). E.g. 'ETR is playing him 8 points "
        f"MORE than the field expects (their coffin number, +8.2)'.\n"
        f"- **Cite everything:** every play / leverage / fade names a SPECIFIC article line OR a "
        f"projection number (own %, ceiling, proj). NO framework-only justification with no "
        f"slate-specific data — if you can't cite it, cut it. But state the citation in plain "
        f"words too: 'Brett's article says his points come almost entirely from a finish'.\n"
        f"- **Readable:** use short tables where they compress; consistent, skimmable structure. "
        f"ONE idea per bullet — expressed fully, not abbreviated.\n\n"
        f"Sections, in THIS order (NO pre-flight/checklist section — that prep is silent):\n"
        f"1. `## The short version` — THE FIRST THING THE USER READS, and the one section that must "
        f"be understandable on its own with no DFS knowledge at all. 6–9 numbered sentences, each a "
        f"SINGLE short sentence, no sub-bullets, no tables, no more than one number per sentence. "
        f"Cover, in this order: (a) what kind of slate this is in one sentence; (b) where the points "
        f"actually come from here, and why; (c) what the crowd is doing; (d) the ONE decision that "
        f"most separates entries this week; (e) what a sharp does differently in one sentence; "
        f"(f) the biggest trap. Every term explained in the same sentence it appears. If someone read "
        f"ONLY this section they should understand the slate. No player tiers here and no citations — "
        f"the detail and the sourcing live in the sections below.\n"
        f"2. `## Slate at a glance` — ≤6 lines: games/fights/races, implied totals or win probs, "
        f"weather, contests + field sizes. A short table, nothing more.\n"
        f"3. `## Edges & tensions` — THE STAR, right up top: the 3–6 things that actually matter this "
        f"slate, SYNTHESIZED — **NOT play/fade calls.** Each is ONE line: **the edge/tension** · the "
        f"cited data that reveals it (article line or number). Surface things like: where the "
        f"scoring/leverage concentrates, an ownership-vs-ceiling mispricing, where the vendors or "
        f"articles DISAGREE, a chalk cluster that's substitutable. **Anchor-Equivalence MUST appear "
        f"here** — but as a SURFACED observation (e.g. 'X and Y are near-identical profiles at "
        f"similar ownership'), NEVER as 'run the alternative.' If the bundle has a `## Field "
        f"tendencies` section, you MUST surface EVERY reliably-crowded cluster it lists here as a "
        f"tension, citing the exact in-N-of-M counts ('the field piles into X/Y in your <type> "
        f"contests, in 3 of 4 — that's where leverage-away lives'). A listed crowd left unsurfaced "
        f"is a coverage leak. If the bundle has a `## Chalk combos` section, you MUST also surface "
        f"its top pairs here as a DUPLICATION tension in plain English — 'the field will pair X + Y "
        f"in roughly N% of lineups (~M lineups in this field); lineups carrying both start the "
        f"night sharing that crowd' (descriptive only; whether to break a pair is the user's call). "
        f"Use NO imperative verbs (no PLAY / FADE / run / cap / pair / build): state the edge and "
        f"stop — the user decides what to do with it. This is the synthesis the user reads first.\n"
        f"4. `## Field vs Sharp — how this slate gets played` — the head-to-head read the user "
        f"builds against: two short cited paragraphs and a punchline, ALL derived from the data.\n"
        f"   - **How the FIELD will play it:** synthesize the mass of lineups' shape from the "
        f"projected ownership (which chalk clusters and salary tiers get jammed — cite the "
        f"breakdown/article reads), the `## Chalk combos` pairs (what most lineups will share), "
        f"and the `## Field tendencies` history (what the field in YOUR contests reliably crowds). "
        f"Be concrete: the anchors, the tiers, the pairings the typical entry will carry.\n"
        f"   - **How a SHARP will play it:** synthesize from the `## Shark reality` envelope "
        f"(own/slot, leverage rate, anchor discipline, uniqueness — the OBSERVED numbers), the "
        f"sharp playbook, and THIS slate's structure: which tier the sharp's anchor comes from, "
        f"where their sub-10%/sub-5% piece lives (use the leverage candidates), and what they "
        f"refuse to share with the field.\n"
        f"   - **The gap:** 1–2 plain sentences naming exactly where the two pictures diverge on "
        f"THIS slate — that divergence is where 'avoid the field, follow the sharp' lives, and it "
        f"should be concrete enough to build from ('the field pays 25% ownership for the $10K "
        f"tier; the sharp gets the same ceiling at 10% in the $9K tier').\n"
        f"   - **How a sharp USES the key players (4–8 of them + the top chalk combos):** for each "
        f"slate-defining player (the jammed chalk anchors, the narrative steamers, the discounted "
        f"elites, the flag-plant tier) give the SHARP'S USAGE in 1–2 plain sentences: their "
        f"exposure stance vs the field (with the number and why — 'the field is at ~30%; a sharp "
        f"runs him underweight around 10% because the ownership is narrative, not projection'), "
        f"the CONSTRUCTION IMPLICATION of using him (the ownership/salary math — 'anchoring him "
        f"at 30% own means the other five slots must average under ~8% to stay inside the sharp "
        f"window; his natural salary partners are exactly the $6K tier the field jams, so a build "
        f"with him needs its uniqueness from elsewhere'), and what a sharp REFUSES around him "
        f"(the chalk combo/pairing the field will share). Same treatment for the top `## Chalk "
        f"combos` pairs: how a sharp handles the combo (skip it / carry at most one side / accept "
        f"it only with the rest of the build unique). This is USAGE GUIDANCE for players the user "
        f"chooses to play — voiced as how the sharp archetype deploys them, with cited numbers. "
        f"It is NEVER a roster, NEVER 'play this lineup,' and NEVER a full combination handed to "
        f"the user — the user picks the players; this teaches how a sharp would hold them.\n"
        f"5. `## Top plays` — tiered **Core / Good / Okay** (same vocabulary as the Player pool; "
        f"Fades live in section 5, not here), one line each: **player** ($sal, own% per source) — "
        f"tier — then 1–2 full plain sentences on WHY, citing the source (article line or number); "
        f"append `· Leverage` to any low-owned high-ceiling play. Clear beats compressed.\n"
        f"6. `## Leverage` — its own section (user directive 7/27/26: leverage and fades are "
        f"SEPARATE sections, never combined). Open with one plain sentence: this section names the "
        f"low-owned players who could decide the slate (the leverage plays). Then the MANDATORY "
        f"screen: for EVERY game/fight/race on the slate, name the single sub-10%-owned high-ceiling "
        f"play — INCLUDING ones the articles never named — with its one-line ceiling path in plain "
        f"words. This is the non-negotiable fix for the recurring miss (the winning sub-10% definer "
        f"that gets faded or never screened). Every spot gets a line. NO fade verdicts in this "
        f"section — fades live in their own section below.\n"
        f"7. `## Fades` — its own section. Open with one plain sentence: this section names the "
        f"popular players whose price in ownership looks too high for what they must do (the fades). "
        f"Then the chalk worth fading, each with the world it needs (a fade is a bet). Name the "
        f"player + verdict in caps (FADE / LEAN FADE / UNDERWEIGHT) and say in plain words what "
        f"each verdict means the first time it appears.\n"
        f"8. `## Key themes` — ≤3 bullets: the structural storylines + where the sources DISAGREE "
        f"(article vs article / vendor vs vendor / article vs projection — that gap is the edge).\n"
        f"9. `## Build it like a sharp` — THE CLOSING SECTION and, with `## The short version`, the "
        f"one the user actually acts on. The user plays **SINGLE ENTRY** almost exclusively: one "
        f"lineup per contest, so each entry is their whole tournament. Their stated goal is to MIMIC "
        f"THE SHARPS. So write this as a numbered walk-through of the decisions a sharp makes, in the "
        f"order they make them, applied to THIS slate.\n"
        f"   SUGGESTIONS ARE WELCOME HERE, in sharp-archetype voice — 'a sharp anchors this slate in "
        f"the $9K tier and takes the cheap dominator', 'a sharp would not carry both halves of that "
        f"pair'. That is explicitly allowed and wanted. What is still FORBIDDEN: telling the USER "
        f"what to do ('you should play X', 'fade Y'), naming a full roster, or presenting any group "
        f"of players as a build. Describe the sharp's reasoning and name candidate players for each "
        f"decision; the user picks.\n"
        f"   Use these numbered steps, each 2–4 SHORT sentences:\n"
        f"   1. **The anchor decision.** Which tier a sharp anchors from here and why the venue or "
        f"format pushes them there. Name the 2–3 realistic anchor candidates with ownership, and note "
        f"which are near-identical (anchor-equivalence) so the user can see the cheaper/less-owned "
        f"side of the same bet.\n"
        f"   2. **The leverage piece.** Where a sharp's low-owned player comes from on THIS slate, "
        f"with 2–4 named candidates and their ownership. Anchor the target to the observed "
        f"`## Shark reality` numbers when that section exists (their real own-per-slot and how often "
        f"they carry a sub-5% player), not the generic playbook. State the user's own gap to that "
        f"number if the data shows one.\n"
        f"   3. **What a sharp refuses.** The specific pairs the field will duplicate most, from the "
        f"`## Chalk combos` and `## Field tendencies` data, with the counts. Say plainly that carrying "
        f"both halves means sharing the entry with roughly N opponents before the race starts.\n"
        f"   4. **The salary shape.** What anchoring at the top costs downstream in plain arithmetic "
        f"— if the anchor takes X of the $50,000, the remaining slots average Y, which lands in "
        f"whichever tier. Note if the slate's chalk cannot all fit under the cap, because then every "
        f"entry must drop one and WHICH one it drops is the real decision.\n"
        f"   5. **Two contests, two different entries.** If the user declared more than one "
        f"single-entry contest, say how a sharp would differentiate them — usually field size and "
        f"payout shape (a bigger, more top-heavy field wants the more contrarian of the two). Each "
        f"entry needs its OWN one-sentence reason it wins; two entries answering the same question "
        f"is one bet paid for twice.\n"
        f"   6. **The pre-lock check.** 3–5 short yes/no questions the user can answer against their "
        f"own built lineup: does it have at least one sub-10% player, is it inside the sharp "
        f"own-per-slot band (cite the observed number), does it avoid both halves of the top "
        f"duplicated pair, can it be explained in one sentence.\n"
        f"   Close with the sharp-envelope target as a one-line summary. If `## Shark reality` names "
        f"individual pros, cite the most relevant one as coaching — e.g. 'moklovin beat you 2 of 3 by "
        f"riding chalk anchors and skipping leverage; the sub-5% piece he never carries is where your "
        f"edge against him lives.'\n\n"
        f"LARGE-FIELD ADDENDUM (MME plan Phase 1): ONLY when the bundle's contest list declares a "
        f"20-Max or 150-Max contest, insert one extra section `## Field attack plan` immediately "
        f"after `## Fades`. Open with one plain sentence: in a big field you win by standing on the "
        f"other side of the crowd's recurring mistakes, not by projecting better. Then, for EACH of "
        f"the field's eight recurring mistakes that has EVIDENCE on THIS slate, write exactly two "
        f"plain sentences: one naming the mistake with this slate's evidence, one naming the attack. "
        f"The eight mistakes (skip any without slate evidence, and say which you skipped in one "
        f"line): (1) the field copies itself — name this slate's likeliest duplicated builds from "
        f"`## Chalk combos`; (2) ownership is mispriced where the public numbers are wrong — the "
        f"cross-vendor disagreements and own-vs-ceiling gaps; (3) the field chases last week's "
        f"highlight (recency) — name who carries narrative ownership without matching equity; "
        f"(4) the field herds onto one of two equal anchors — the anchor-equivalence twins, and in "
        f"a big field the underowned twin is a SIZED bet, not one lineup's pivot; (5) the field "
        f"skips the mid-price scorer tier — name this slate's ignored-tier players (the leverage "
        f"list); (6) part of the field builds dead lineups (MMA: both sides of a fight; NASCAR: "
        f"two max-dominator bets) — one line on what dead structure looks like here; (7) the field "
        f"stampedes on unconfirmed news — only if live this slate; (8) the trap plays losers love "
        f"— from `## Field tendencies` / fish-trap history when present. Close the section with one "
        f"sentence: the effective field is smaller than the listed size because of these mistakes. "
        f"STILL ZERO LINEUPS — this is a target list the user attacks in the Sim tool. The 5th-grade "
        f"writing rules apply here like everywhere.\n\n"
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

    # Same numbers as the deterministic pass, so the two graders can never
    # argue: the tab once green-lit a lineup (under the calibrated flag line)
    # while this thesis check dinged it against the strategy's aspirational
    # "~13% envelope" pulled from prose.
    cal_line = ""
    try:
        from src import grader as _grader
        from src.contests import load_contests as _load_contests
        _cal = _grader.calibration(slug, sport, _load_contests(slug))
        _tgt = _cal.get("shark_own") or _cal.get("winners_own")
        _flag = _cal.get("own_flag_above")
        if _flag is not None:
            cal_line = (
                f"Ownership calibration (the deterministic grader's own data-derived numbers — "
                f"use THESE, never an envelope re-derived from the strategy text): sharp target "
                f"≈ {_tgt}% average ownership per slot; a lineup is chalk-heavy only ABOVE "
                f"{_flag}%. Do not name ownership as a weakness for any lineup at or below "
                f"{_flag}%.\n\n"
            )
    except Exception:  # noqa: BLE001 — calibration context is additive
        cal_line = ""

    prompt = (
        cal_line +
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
        f"lineups triggers, or 'None.' State the lesson as one plain sentence about what keeps "
        f"happening and why (the mechanism) — the lesson id may follow in parentheses.\n"
        f"WRITING STYLE (user directive 7/27/26 — write for a smart 5th grader; more words is "
        f"fine): short sentences, one idea each (~15 words, hard stop 25). Say the plain meaning "
        f"FIRST with the DFS word in parentheses after, every time — 'the players most teams "
        f"will pick (the chalk)'. Explain what each number means: '32% owned — about 1 in 3 "
        f"teams has him'. Open each section with one sentence saying what it is for. "
        f"NO play/fade commands, NO alternative "
        f"lineups, NO swap suggestions. Do not ask questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_player_pool(slug: str, contest_label: str, sport: str) -> dict:
    """Build the ranked, annotated player pool: EVERY rosterable player from
    the loaded projections (fades stay on the board tiered `Fade`), ranked for
    GPP with a short write-up each. Membership is computed deterministically here; Claude only
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
           "'How it wins' is a SHORT PLAIN-ENGLISH phrase (~10–15 words) a non-expert reads "
           "instantly — NEVER jargon codes like 'coffin +7.6' or ranking shorthand — and Tier "
           "carries any `· Leverage` label.\n"
           if is_mma else
           "`| Rank | Player | Sal | Proj | Own | How it wins | Tier |`, where 'How it wins' is a "
           "SHORT PLAIN-ENGLISH phrase (~10–15 words) a non-expert reads instantly — NEVER jargon "
           "codes like 'coffin +7.6' or ranking shorthand — and Tier carries any `· Leverage` "
           "label.\n") +
        f"- THEN a single continuous numbered list (the detailed write-ups), best to worst. "
        f"Each entry LEADS WITH THE DATA, tier LAST as a one-word read:\n"
        f"  `**N. Player Name** — $salary, own% (per source), proj X[, ceiling Y]` then a 2–4 "
        f"sentence synthesis in PLAIN, COMPLETE ENGLISH: how it wins (the ceiling path / the edge) "
        f"+ the key risk or condition. Write for a smart 5th grader (user directive 7/27/26) — "
        f"more words is totally fine, confusion is not. "
        f"**ONE IDEA PER SENTENCE, ~15 words, hard stop at 25.** Do not chain clauses with "
        f"semicolons or dashes into one long sentence, and never stack more than two numbers in a "
        f"sentence — split it. **Say the plain meaning FIRST and put the DFS word in parentheses "
        f"after, EVERY time it appears** — 'the players most teams will pick (the chalk)', 'his "
        f"best realistic night (his ceiling)' — never assume a term stuck from an earlier "
        f"write-up. Explain what numbers MEAN: '34% owned — about 1 of every 3 teams will have "
        f"him'. NEVER print a vendor term "
        f"(coffin, dock, boost, sim-optimal, steam) without saying what it means in the SAME "
        f"sentence — e.g. 'ETR is playing him 8 points MORE than the field expects (their coffin "
        f"number, +8.2)'. NEVER print an internal source code such as 'image-35', 'DDD' or 'DFR' — "
        f"name the source in words ('the practice-speed chart', \"Dustin's Deep Dive\"). END the "
        f"line with `— <tier>` (+ `· Leverage` if it applies). Slate-specific, no filler, no "
        f"play/fade command.\n"
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


def run_autopsy_review(slug: str, contest_label: str, sport: str, hist_dir=None) -> dict:
    """Post-autopsy learning run: grade the archived slate's process, update
    the lesson ledger + venue file, and write proposed (not applied)
    framework changes to <history_dir>/autopsy_review.md."""
    from src.history import latest_history_dir

    # PINNED: the caller passes the directory it displayed. Both this and the
    # UI used to call latest_history_dir() independently, so a slate logged
    # between render and click meant reviewing/applying a DIFFERENT slate than
    # the one on screen. That is how a week-old card got reviewed twice.
    hist_dir = Path(hist_dir) if hist_dir else latest_history_dir(slug)
    if hist_dir is None:
        return {"ok": False, "error": "No archived slate found — log an autopsy first.",
                "duration_s": 0.0, "cost_usd": None}

    # Ledger-hygiene flags ride the post-autopsy review (the loop that actually
    # runs every slate) instead of a separate optional button — the standalone
    # ledger review ran once in 18 slates and its stale proposals were a
    # one-click hazard. Deterministic flags are computed fresh here, so the
    # review always reasons against the CURRENT ledger.
    hygiene_md = ""
    try:
        from src import ledger_hygiene
        hygiene_md = ledger_hygiene.report_md(ledger_hygiene.hygiene_report(slug))
    except Exception:  # noqa: BLE001 — hygiene is additive, never blocks the review
        hygiene_md = ""

    out_path = hist_dir / "autopsy_review.md"
    prompt = (
        f"Run the post-autopsy review for the archived {contest_label} slate at `{hist_dir}`. "
        f"Read its manifest.json, slate_analysis.md, autopsy.json, and results.json, "
        f"the shark head-to-head at `{hist_dir}/shark_gap.json` (structural you-vs-the-pros), "
        f"the own-strategy adherence grade at `{hist_dir}/adherence.json` (if present), "
        f"the player-pool tier calibration at `{hist_dir}/pool_calibration.json` (if present — "
        f"did the board's tiers hold up, and who got buried?), "
        f"the Sim's autopsy measurements at `{hist_dir}/sim_autopsy.json` (if present — one payload "
        f"per contest: pool-vs-picking stats and whether each pre-lock sim ranking metric actually "
        f"predicted real finishes), "
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
        f"1c2. POOL VS PICKING (only when `sim_autopsy.json` exists): from each contest's payload, "
        f"answer the question the standings alone cannot — was the miss in GENERATION (the built "
        f"pool never held a winning-caliber lineup) or SELECTION (the pool held one, the picks "
        f"missed it)? Use pool.max_actual vs the winning score, n_beating_best_entry (with 5,000 "
        f"lineups, hindsight always finds gems — judge the RATE, not the existence), and "
        f"picking_edge_points (positive = the picks beat the pool average). Also read rank_signal: "
        f"a spearman near 0 means that sim metric gave NO edge that slate — if the SAME metric "
        f"reads near-zero or negative across multiple archived slates, that is a tool-calibration "
        f"finding worth a lesson (the sim is a threshold, not a gospel ranking). One slate is noise.\n"
        f"1d. CODIFIED-RULE CHECK: for each lesson in `rules/{slug}/lessons.yaml` with status "
        f"'codified', note whether the archived strategy actually APPLIED it (or it didn't trigger "
        f"this slate) and whether its MECHANISM held against the DK actuals. Codification is not "
        f"tenure: a codified rule whose mechanism has now failed in 2+ slates gets a demotion "
        f"proposal in '## Proposed codifications' (retire or narrow its scope), with the exact "
        f"framework.md edit. Same GPP guard — a lost contest alone is not a mechanism failure.\n"
        + (
            f"1e. LEDGER HYGIENE: a deterministic pre-pass flagged these ledger-maintenance "
            f"candidates:\n{hygiene_md}\nFor each STALE hypothesis decide RETIRE or KEEP with a "
            f"one-line mechanism reason (GPP guard: a lesson untested only because no RELEVANT "
            f"slate occurred is KEEP, not retire; name the retired_reason if retiring). For each "
            f"NEAR-PROMOTION lesson name the exact mechanism a third slate must confirm. For each "
            f"OVERDUE promotion include the codification edit in '## Proposed codifications'. For "
            f"each MERGE pair decide MERGE or KEEP-SEPARATE (if merge: which id survives + the "
            f"combined statement — merges also go in '## Proposed codifications'). Also retire any "
            f"lesson whose mechanism references a REMOVED feature that can no longer fire. Write "
            f"the decisions under a '## Ledger hygiene' section in the review.\n"
            if hygiene_md else ""
        )
        + f"2. UPDATE `rules/{slug}/lessons.yaml` directly (Edit tool): add confirmations/contradictions "
        f"with this slate's date and history dir; promote status to 'validated' where confirmations "
        f"exist; add new 'hypothesis' lessons born from this autopsy — mechanism-based, not "
        f"result-based. A recurring shark-gap axis (1b) should birth or confirm a mechanism lesson.\n"
        f"3. UPDATE THE VENUE FILE for this slate's venue (sport `{sport}`; see CLAUDE.md for the "
        f"venue dir; create the file from the archived strategy if missing): append a date-stamped "
        f"'Per-slate observation' line with what this slate proved or disproved about the venue.\n"
        f"4. WRITE `{out_path}` with sections: '## Process scorecard', '## Lesson ledger changes', "
        f"'## Venue file changes', '## Ledger hygiene' (the 1e decisions; omit the section if there "
        f"were no flags), and '## Proposed codifications' — for any lesson meeting the "
        f"promotion criteria (3 confirming slates) write the exact framework.md/philosophy.md edit "
        f"you propose; for retirement candidates (2 mechanism contradictions) the same. If nothing "
        f"qualifies, write 'None this slate.' under that heading. "
        f"Do NOT edit framework.md or philosophy.md in this run — proposals only; the user approves.\n"
        f"GPP guard: a bad ROI or a lost contest is NEVER a contradiction by itself; only mechanism "
        f"failures count. Do not ask any questions — produce the file.\n\n"
        f"HOW TO WRITE THE REVIEW (user directive 7/27/26 — the review must read like it was "
        f"written for a smart 5th grader; more words is totally fine):\n"
        f"- Keep the EXACT section headers listed above (the app reads them by name), but under "
        f"every header, START with one plain sentence saying what the section is about. Example "
        f"under '## Process scorecard': 'This section grades HOW you played the slate — the "
        f"decisions, not the results.'\n"
        f"- Short sentences, ordinary words, one fact per sentence (~15 words, hard stop 25). No "
        f"semicolon chains. No more than two numbers in a sentence.\n"
        f"- Say the plain meaning FIRST and put the DFS or ledger word in parentheses after, EVERY "
        f"time it appears: 'the low-owned player who could decide the slate (the definer)', 'an "
        f"idea we are still testing (a hypothesis lesson)', 'a rule that has proven itself and now "
        f"lives in your framework (codified)', 'whether your entries followed your own plan "
        f"(adherence)', 'the reason WHY something happens (the mechanism)'. Never assume a term "
        f"stuck from an earlier section — the user has said the verbiage loses him.\n"
        f"- Explain what every number MEANS: not 'best percentile 3.5' but 'your best entry beat "
        f"96.5% of the field (top 3.5%)'. Not '0 of 2 leverage candidates' but 'the strategy named "
        f"2 low-owned players who could decide the slate, and none of your entries had either one'.\n"
        f"- When you grade something as good or bad, say in one plain sentence WHAT TO DO ABOUT IT "
        f"next slate. A grade without a next step is just a scold.\n"
        f"- End the whole review with a section '## What this means for next slate' — 3-5 numbered, "
        f"single-sentence takeaways a 5th grader could follow, most important first."
    )
    # lessons.yaml is a collateral edit of this run — snapshot/restore + parse
    # gate. The venue file is append-mostly and its path isn't statically
    # known, so it stays unsnapshotted.
    return _run_claude(prompt, out_path,
                       collateral=[_REPO_ROOT / "rules" / slug / "lessons.yaml"])


def run_apply_proposals(slug: str, hist_dir=None) -> dict:
    """Apply the user-approved '## Proposed codifications' from the latest
    autopsy review to framework.md/philosophy.md + the lesson ledger."""
    from src.history import latest_history_dir

    # PINNED: the caller passes the directory it displayed. Both this and the
    # UI used to call latest_history_dir() independently, so a slate logged
    # between render and click meant reviewing/applying a DIFFERENT slate than
    # the one on screen. That is how a week-old card got reviewed twice.
    hist_dir = Path(hist_dir) if hist_dir else latest_history_dir(slug)
    review_path = hist_dir / "autopsy_review.md" if hist_dir else None
    if review_path is None or not review_path.exists():
        return {"ok": False, "error": "No autopsy review found — run the review first.",
                "duration_s": 0.0, "cost_usd": None}

    prompt = (
        f"Read `{review_path}`, sections '## Proposed codifications' and '## Ledger hygiene' (if "
        f"present). The user has APPROVED these proposals. Apply each proposed edit to "
        f"`rules/{slug}/framework.md` / "
        f"`rules/{slug}/philosophy.md` exactly as written, then update `rules/{slug}/lessons.yaml`: "
        f"set the affected lessons' status to 'codified' (with codified_in naming the doc + section) "
        f"or 'retired' (with retired_reason). For '## Ledger hygiene' decisions: apply each RETIRE "
        f"(status 'retired' + the named retired_reason) and each MERGE (keep the surviving id with "
        f"the combined statement; set the other to 'retired' with retired_reason 'merged into "
        f"<id>'); leave every KEEP / KEEP-SEPARATE lesson untouched. Finally append a line "
        f"'## Applied' with the current changes summarized to the end of `{review_path}`. "
        f"Do not ask any questions."
    )
    rules_dir = _REPO_ROOT / "rules" / slug
    return _run_claude(prompt, review_path,
                       collateral=[rules_dir / "framework.md",
                                   rules_dir / "philosophy.md",
                                   rules_dir / "lessons.yaml"])


# The standalone ledger review (run_ledger_review / run_apply_ledger_proposals)
# was folded into run_autopsy_review (step 1e) + run_apply_proposals on 7/18/26:
# the optional button ran once in 18 slates, and a stale rules/<slug>/
# ledger_review.md sat behind an always-armed Approve button. Hygiene flags now
# ride the loop that actually runs every slate.
