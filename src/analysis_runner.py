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
        f"is leverage signal (surface it in Edges & tensions / the Leverage section).\n\n"
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
        f"HARD RULE — A TRAP IS A PRICE, NOT A PLAYER (user directive 8/9/26): NEVER justify a "
        f"fade or underweight with a cross-slate name count ('he was a trap in 2 of 3'). A player "
        f"cannot be a trap — his salary, projection, and ownership change every slate. Justify "
        f"every fade/underweight with THIS slate's numbers: a same-projection peer at lower "
        f"ownership, or ownership ranking ahead of projection rank (see the bundle's "
        f"`## Trap-shaped prices` section when present). History informs the FIELD'S behavior "
        f"(where your opponents go); it never informs a player's quality.\n\n"
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
        f"it's for a 5th grader', UPDATED 8/9/26: the doc must ALSO be SHORT — the old 'more words "
        f"is totally fine' is revoked; a 6,000-word brief takes 25 minutes to read and the user "
        f"asked for compact, simple, straightforward):\n"
        f"- **Write for a 5th grader. This is the master rule.** Short sentences. Ordinary words. "
        f"One fact at a time. After you write each sentence, ask: would a smart 11-year-old have to "
        f"re-read this, or ask what a word means? If yes, REWRITE IT. Clarity wins every tie — but "
        f"say it ONCE, in the fewest plain words that stay clear.\n"
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
        f"Density AND length are both enemies — one idea per sentence, and no idea said twice.\n"
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
        f"place differential, fish trap (a PRICE the losing half buys — never a player), "
        f"own-per-slot, stars-and-scrubs, punt, and every vendor term "
        f"(coffin, dock, boost, sim-optimal, steam, exposure). E.g. 'ETR is playing him 8 points "
        f"MORE than the field expects (their coffin number, +8.2)'.\n"
        f"- **Cite everything:** every play / leverage / fade names a SPECIFIC article line OR a "
        f"projection number (own %, ceiling, proj). NO framework-only justification with no "
        f"slate-specific data — if you can't cite it, cut it. But state the citation in plain "
        f"words too: 'Brett's article says his points come almost entirely from a finish'.\n"
        f"- **Readable:** use short tables where they compress; consistent, skimmable structure. "
        f"ONE idea per bullet — expressed fully, not abbreviated.\n\n"
        f"LENGTH BUDGET (raised 8/29/26 by the user to **5,000 words** for the whole "
        f"document; previously 2,200): aim for 3,000–4,500. The extra room exists to make "
        f"things CLEARER, never longer. Spend it on: explaining what a number MEANS, walking "
        f"through the reasoning step by step, and saying what the field is likely to do and how "
        f"this slate beats it. Suggested spend — Short version ~250 · Slate at a glance ~150 · "
        f"Edges & tensions ~500 · Field vs Sharp ~700 (this is the home of 'what the field will do') · Top plays "
        f"~900 · Leverage ~500 · Fades ~350 · Build it like a sharp ~600, with the remaining "
        f"headroom going to whichever section this slate genuinely needs. Trim by SELECTION — "
        f"delete whole repeated ideas, never blur a claim to save words.\n"
        f"**MORE ROOM IS NOT PERMISSION TO GET COMPLICATED.** The 5th-grader rule above still "
        f"governs every single sentence at 5,000 words exactly as it did at 2,200. If a longer "
        f"document is harder to read than a shorter one would have been, it is WORSE and you "
        f"have misused the budget. Use the space for more short sentences, not longer ones.\n\n"
        f"NEVER VAGUE (user directive 8/11/26): every claim names its subject AND its numbers. "
        f"Never 'the top scorer' without the player's name; never 'a cheap golfer spiked' "
        f"without who, salary, and score; never 'the screen missed him' without the number it "
        f"missed by. If cutting words would cost a claim its name or number, keep the words.\n\n"
        f"ONE HOME PER PLAYER: each player is EXPLAINED in exactly ONE section — almost always "
        f"`## Top plays` (leverage plays in `## Leverage`, fades in `## Fades`). Everywhere else he "
        f"appears as his NAME plus at most five words ('Jones — the fight-3 leverage piece'). If "
        f"you explained him once, you are done explaining him. Never write a second paragraph "
        f"about the same player — repetition is where the old 6,000-word briefs came from.\n\n"
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
        f"3. `## Edges & tensions` — THE STAR, right up top: the things that actually matter this "
        f"slate, SYNTHESIZED — **NOT play/fade calls.** A numbered list, **max 8 lines, each ONE "
        f"line of at most ~20 words**: **the edge/tension** · the cited data that reveals it "
        f"(article line or number). Grow to 10 lines ONLY if the mandates below need the room. "
        f"Candidates: where scoring/leverage concentrates, an ownership-vs-ceiling mispricing, "
        f"where vendors or articles DISAGREE (that gap IS the edge — this replaces the old "
        f"`## Key themes` section, which no longer exists), a substitutable chalk cluster. "
        f"MANDATES (each gets ONE line, never a paragraph): **Anchor-Equivalence MUST appear** — "
        f"as an observation ('X and Y near-identical at similar own'), never 'run the "
        f"alternative'; if the bundle has `## Field tendencies`, EVERY reliably-crowded cluster "
        f"it lists gets a line with its in-N-of-M count, framed ONLY as opponent behavior "
        f"('your opponents pile onto X/Y, in 3 of 4') — never player quality, never fade "
        f"evidence — plus one line for its trap SHAPE (the price conditions losers keep buying); "
        f"if the bundle has `## Trap-shaped prices`, its THIS-slate names get a line; if the "
        f"bundle has `## Chalk combos`, the top pair gets a duplication line ('the field pairs "
        f"X + Y in ~N% of lineups, ~M in this field'). A listed crowd or leverage candidate left "
        f"unsurfaced is a coverage leak. NO imperative verbs (no PLAY / FADE / run / cap / pair "
        f"/ build): state the edge and stop — the user decides.\n"
        f"4. `## Field vs Sharp — how this slate gets played` — the head-to-head read the user "
        f"builds against, in THREE short parts, ~180 words total, ALL derived from the data. "
        f"Players by NAME only here — their explanations live in `## Top plays`.\n"
        f"   - **How the FIELD will play it (~2 sentences):** the mass of lineups' shape from "
        f"projected ownership, the `## Chalk combos` pairs, and `## Field tendencies` history — "
        f"the anchors, tiers, and pairings the typical entry carries.\n"
        f"   - **How a SHARP will play it (~2 sentences):** from the `## Shark reality` envelope "
        f"(own/slot, leverage rate, anchor discipline, uniqueness — the OBSERVED numbers) applied "
        f"to THIS slate: the sharp's anchor tier, where their sub-10% piece lives, what they "
        f"refuse to share with the field.\n"
        f"   - **The gap (1–2 sentences):** exactly where the two pictures diverge on THIS slate, "
        f"concrete enough to build from ('the field pays 25% ownership for the $10K tier; the "
        f"sharp gets the same ceiling at 10% in the $9K tier').\n"
        f"   (The old sub-part (d) — a second per-player usage essay — is DELETED 8/9/26: it "
        f"restated `## Top plays` in different words. The sharp's stance on each key player now "
        f"lives as the one-line 'sharp stance' inside `## Top plays`.)\n"
        f"5. `## Top plays` — **the ONE home for every player write-up.** Tiered **Core / Good / "
        f"Okay** (same vocabulary as the Player pool; Fades live in `## Fades`). **At most 12 "
        f"players**, best table-formatted, one row each: **player** ($sal, own%) — tier — ONE "
        f"plain sentence (~20 words max) on WHY, citing its source — plus a short **sharp "
        f"stance** for the slate-defining ones ('field ~30%, a sharp runs ~10% — narrative "
        f"ownership'). Append `· Leverage` to any low-owned high-ceiling play. Twelve rows the "
        f"user remembers beat twenty-five he skims.\n"
        f"6. `## Leverage` — its own section (user directive 7/27/26: leverage and fades are "
        f"SEPARATE sections, never combined). Open with one plain sentence: this section names the "
        f"low-owned players who could decide the slate (the leverage plays). Then the MANDATORY "
        f"screen: for EVERY game/fight/race on the slate, name the single sub-10%-owned "
        f"high-ceiling play — INCLUDING ones the articles never named. **ONE flat list, ONE line "
        f"per spot, ~15 words max per line** ('**Name** ($sal, own%) — his ceiling path in plain "
        f"words'). NO sub-headers, NO price-band subsections, NO paragraphs. Every spot gets its "
        f"line — the screen is the non-negotiable fix for the recurring faded-winning-definer "
        f"miss — but a line is ALL each spot gets. NO fade verdicts here.\n"
        f"7. `## Fades` — its own section. Open with ONE plain sentence explaining what the three "
        f"verdicts mean, once for the whole section: FADE = play him nowhere, LEAN FADE = mostly "
        f"avoid, UNDERWEIGHT = use him less than the crowd does, never zero. Then one line per "
        f"player: **NAME — VERDICT** — one ~20-word sentence citing THIS slate's salary + "
        f"projection + ownership (a cheaper same-projection peer, or ownership outrunning "
        f"projection rank) and the world the fade needs. NEVER cite a past-slate name count as "
        f"fade evidence — a trap is a price, not a player.\n"
        f"8. `## Build it like a sharp` — THE CLOSING SECTION and, with `## The short version`, the "
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
        f"   Use these numbered steps, **each 1–2 SHORT sentences — players by NAME only, no "
        f"re-explaining anyone (their write-ups live in `## Top plays`)**:\n"
        f"   1. **The anchor decision.** The tier a sharp anchors from and why. The 2–3 anchor "
        f"candidates with ownership, flagging any anchor-equivalence twins.\n"
        f"   2. **The leverage piece.** Where the sharp's low-owned player comes from, 2–4 named "
        f"candidates with ownership, target anchored to the observed `## Shark reality` numbers "
        f"when present.\n"
        f"   3. **What a sharp refuses.** The top duplicated pair(s) with counts — 'carrying both "
        f"means sharing the entry with ~N opponents before it starts.' Pair counts describe the "
        f"FIELD's habit, never the players' quality.\n"
        f"   4. **The salary shape.** The anchor's downstream cost in plain arithmetic — anchor "
        f"takes $X, the other slots average $Y. If the chalk cannot all fit under the cap, say "
        f"WHICH-one-to-drop is the real decision.\n"
        f"   5. **Two contests, two different entries.** Only if 2+ contests are declared: how a "
        f"sharp differentiates them by field size and payout shape, each entry with its own "
        f"one-sentence reason it wins.\n"
        f"   6. **The big-field attack** — ONLY when the bundle's contest list declares a 20-Max "
        f"or 150-Max contest (this replaces the old separate `## Field attack plan` section, "
        f"deleted 8/9/26). One line, ~15 words, per field mistake that has evidence on THIS "
        f"slate — mistake · evidence · attack. The catalog to screen: self-copying (chalk "
        f"combos), mispriced ownership, recency chasing, anchor-twin herding, ignored mid-price "
        f"tier, dead builds, news stampedes, trap-shaped prices (never a cross-slate name "
        f"count). Skip silent mistakes without listing them. Close: the effective field is "
        f"smaller than the listed size. Still ZERO lineups.\n"
        f"   7. **The pre-lock check.** 3–5 short yes/no questions against the built lineup, and "
        f"EVERY question must come from THIS slate's own reads — the anchor decision above, a "
        f"pair the field duplicates, a fade the strategy named, the lineup's one-sentence thesis. "
        f"**NEVER write a question that requires a player for being low-owned** ('at least one "
        f"sub-10% player', 'has a leverage piece', 'inside the own-per-slot band'). The pros carry "
        f"a low-owned piece at a RATE across their entries, not in every lineup, and contest "
        f"winners regularly carry none — so a lineup with no low-owned player fails nothing. "
        f"Ownership belongs in these questions only as THIS slate's specific read (e.g. 'does it "
        f"avoid both halves of the pair the field will duplicate?'), never as a threshold a roster "
        f"must clear.\n"
        f"   Close with the sharp-envelope target in ONE line, citing the most relevant named pro "
        f"from `## Shark reality` as coaching where one exists.\n\n"
        f"Do not ask any questions — read the inputs and produce the file."
    )
    return _run_claude(prompt, out_path)


def run_grade(slug: str, contest_label: str, sport: str, lineups_text: str,
              contest: dict | None = None, file_key: str | None = None) -> dict:
    """Thesis check for lineups (the Grade tab's claude pass, on top of the
    deterministic checks in src/grader.py). For each pasted lineup: a one-line
    'how it wins' thesis grounded in the slate data — or THESIS-LESS — plus a
    distinctness read. GRADES ONLY: never builds, swaps, or fixes.

    PER-CONTEST mode (8/9/26 — not every contest is the same): pass `contest`
    (a declared-contest dict) + `file_key` and the grade judges the lineups
    against THAT contest only (its field size, payout shape, and comparable
    history), writing data/grade/<slug>__<file_key>.md. Without them: the
    legacy pooled grade at data/grade/<slug>.md."""
    if contest is not None and file_key:
        out_path = _REPO_ROOT / "data" / "grade" / f"{slug}__{file_key}.md"
    else:
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
        if contest is not None:
            _cal = _grader.contest_calibration(slug, sport, contest)
        else:
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

    contest_line = ""
    if contest is not None:
        _shape = contest.get("payout_shape") or "not declared"
        contest_line = (
            f"This grade is for ONE contest only: \"{contest.get('name')}\" — field "
            f"{int(contest.get('field_size') or 0):,} entrants, ${contest.get('entry_fee')} "
            f"entry, payout shape {_shape}, {contest.get('my_entries')} entry(ies). "
            f"Judge every lineup against THIS contest: a top-heavy payout needs a "
            f"first-place story; a flat payout needs a safe-floor story. Do not compare "
            f"against other contests.\n\n"
        )

    n_lineups = len([l for l in (lineups_text or "").splitlines() if l.strip()])
    distinct = (
        f"2. `## Distinctness` — do the lineups answer DIFFERENT what-ifs? Name any pair that "
        f"answers the same question (competing lineups).\n" if n_lineups > 1 else "")
    prompt = (
        cal_line + contest_line +
        f"You are grading the user's {contest_label} DK lineups (sport: {sport}) "
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
        + distinct +
        f"3. `## Lessons that activate` — any open lesson from lessons.yaml this set of "
        f"lineups triggers, or 'None.' State the lesson as one plain sentence about what keeps "
        f"happening and why (the mechanism) — the lesson id may follow in parentheses.\n"
        f"WRITING STYLE (user directives 7/27/26 write for a smart 5th grader + 8/9/26 keep it "
        f"SHORT — say each thing once): short sentences, one idea each (~15 words, hard stop 25). Say the plain meaning "
        f"FIRST with the DFS word in parentheses after, every time — 'the players most teams "
        f"will pick (the chalk)'. Explain what each number means: '32% owned — about 1 in 3 "
        f"teams has him'. Open each section with one sentence saying what it is for. "
        f"NO play/fade commands, NO alternative "
        f"lineups, NO swap suggestions. Do not ask questions — produce the file."
    )
    return _run_claude(prompt, out_path)


def run_contest_selection(slug: str, contest_label: str, sport: str,
                          sim_label: str) -> dict:
    """Claude PICKS one contest's entries from that contest's candidate slice
    of the Sim's pool (8/9/26 — per-contest selection; not every contest is
    the same).

    Selection is not construction: the slice is ~100 REAL pool rows with THIS
    contest's own sim numbers; Claude chooses rows BY ID. The app then runs
    `lineup_selection.parse_pick`, which rejects fabricated ids, modified
    rosters, and wrong counts — a bad pick saves nothing.

    Writes data/lineup_selection/<slug>__<key>_pick.md (slice digest beside
    it). Returns {ok, error, duration_s, cost_usd, key, sim_label}."""
    from src import lineup_selection as ls, sim_link
    from src.contests import load_contests as _load_contests

    pool = sim_link.load_sim_pool(slug)
    if not pool:
        return {"ok": False, "error": "No Sim pool — send it from the Sim's "
                "Lineups or Portfolio tab first.", "duration_s": 0.0,
                "cost_usd": None}
    sim_contest = next((c for c in pool.get("contests") or []
                        if str(c.get("label")) == str(sim_label)), None)
    if sim_contest is None:
        return {"ok": False, "error": f"Contest '{sim_label}' is not in the "
                "Sim's pushed pool.", "duration_s": 0.0, "cost_usd": None}

    declared = ls.match_contests(pool.get("contests") or [],
                                 _load_contests(slug)).get(str(sim_label))
    key = ls.contest_file_key(sim_label, declared)
    # THE STRATEGY GUIDE (8/29/26, was a hard gate 8/15-8/29): every lineup
    # is pickable; a rule break is a priced cost the pick must defend in
    # writing. No strategy contract => nothing to weigh against => no pick.
    gate = ls.strategy_gate(slug)
    if not gate.get("has_contract"):
        return {"ok": False, "error": "No slate strategy for this slate — picks "
                "must follow it. Generate the slate strategy first (Slate "
                "Strategy tab), then pick.", "duration_s": 0.0, "cost_usd": None}
    elig = ls.eligible_indexes(pool, gate)
    if not elig["allowed"]:
        # Since 8/29/26 `allowed` is the whole pool, so this only fires on an
        # EMPTY pool. The old message ("no lineup follows the strategy") would
        # now be actively wrong — strategy breaks no longer remove rows.
        return {"ok": False, "error": "The Sim's pool is empty for this slate — "
                "build and send a pool first.", "duration_s": 0.0,
                "cost_usd": None}
    # One lineup, one contest (8/15/26): lineups already picked for another
    # contest on this slate are cut from the slice, so Claude never sees them.
    taken = ls.taken_roster_keys(slug, pool, exclude_label=str(sim_label))
    rows = ls.candidate_slice(pool, sim_contest,
                              strategy=ls.strategy_slice_names(slug),
                              taken=taken, allowed=elig["allowed"], gate=gate)
    if not rows:
        return {"ok": False, "error": "The pool has no rows for this contest.",
                "duration_s": 0.0, "cost_usd": None}
    # `contest` prices each hard rule by the SIM QUALITY it deletes, not just
    # the count; `num_simulations` sizes the Top-1% tie band (both 8/29/26).
    gate_md = ls.gate_summary(gate, elig, pool=pool, contest=sim_contest)
    slice_p = ls.slice_path(slug, key)
    slice_p.parent.mkdir(parents=True, exist_ok=True)
    slice_p.write_text(ls.slice_digest_md(slug, str(sim_label), sim_contest,
                                          declared, rows,
                                          pool.get("ownership") or {},
                                          gate_md=gate_md,
                                          sims=pool.get("num_simulations")))
    out_path = ls.pick_path(slug, key)
    bundle_path = build_bundle(slug, contest_label, sport)
    my = int(sim_contest.get("my_entries") or 1)
    shape = (declared or {}).get("payout_shape") or "not declared"
    # A pool sent without a simulation (8/29/26): the metrics arrays are
    # absent, the table ranks on projection + ownership, and the prompt must
    # neither cite sim numbers nor let Claude invent them.
    no_sim = all(r.get("top1_pct") is None for r in rows)

    if no_sim:
        _metric_block = (
            "How to think about THIS contest — with NO sim numbers:\n"
            "- This pool was never simulated. The table carries projected "
            "points, salary, and ownership only; the win/top1/cash/roi "
            "columns are empty dashes. Do not invent, estimate, or imply a "
            "sim number anywhere — argue from what is on the table.\n"
            "- The table is ranked on a blend of projected points and "
            "ownership. That ranking says a lineup is strong and says how "
            "popular it is; it does NOT say it wins. Rank order matters even "
            "less than usual here — read lineup shapes, not table "
            "positions.\n"
            "- Duplication: the dupes column (when present) estimates how "
            "many opponents hold the same lineup. Being alone on a winner "
            "beats sharing it.\n"
            "- **PROJECTED POINTS IS STILL A QUALIFIER, NOT THE HEADLINE** "
            "(user directive 8/29/26). Scale each slate so its best possible "
            "lineup = 100: across 14 slates the typical contest WINNER "
            "projected 94 and the typical ENTRY projected 94 too — winners "
            "sit in the same place on the projection scale as the field. Use "
            "projection to confirm a lineup belongs; choose on OWNERSHIP "
            "SHAPE and slate dynamics — where the lineup steps away from the "
            "crowd and what has to happen for that step to pay.\n")
        _why_block = (
            "**Why these picks:** <THE MAIN OUTPUT. A cohesive argument, not "
            "a list of numbers (user directive 8/29/26). There are NO sim "
            "numbers on this slate, so it must pull FOUR things together "
            "into one read, and it must show how they connect:\n"
            "  1. **Slate dynamics** — WHAT YOU THINK THE FIELD IS DOING, "
            "and HOW THIS LINEUP BEATS IT. The spine of the argument: say "
            "who the crowd is piling onto and why, then where this lineup "
            "steps away from that crowd and what has to happen for the step "
            "to pay.\n"
            "  2. **Ownership** — how many other teams will look like this, "
            "player by player where it matters.\n"
            "  3. **Projected points** — a check that the lineup is strong "
            "enough to belong, NOT the reason to pick it.\n"
            "  4. **Duplication** — when the dupes column exists, whether "
            "anyone else holds this exact lineup.\n"
            "Where two of them DISAGREE, say so and say which one you "
            "trusted. Never cite a win%, top1%, cash%, or ROI number — none "
            "exists for this pool, and a made-up one fails the pick.\n"
            "Length: 6-12 short sentences. Every number gets its plain "
            "meaning in the SAME sentence — '38% owned means about 4 of "
            "every 10 teams have him'. Plain meaning FIRST, the DFS word in "
            "parentheses after — 'picked by few teams (low-owned)'. Write it "
            "so a 5th grader follows the whole argument start to finish: "
            "short sentences, one idea each, no clause chains. If the pick "
            "carries a `cost`, this is also where you name the player and "
            "the rule and defend the override.>\n\n")
    else:
        _metric_block = (
            "How to think about THIS contest (its numbers, not another "
            "contest's):\n"
            "- The payout shape decides the metric that matters most. "
            "Top-heavy: the chance to finish 1st (the top1% column). Flat or "
            "Balanced: the chance of any payout (the cash% column). Not "
            "declared: balance the two.\n"
            "- Small fields (under ~2,500 entrants) reward the steadier "
            "ceiling — the win% column matters more there.\n"
            "- Duplication: the dupes column (when present) estimates how "
            "many opponents hold the same lineup. Being alone on a winner "
            "beats sharing it.\n"
            "- **Sim ROI** is what the simulation thinks the entry is worth "
            "against THIS contest's payout ladder — it already folds the "
            "field and the prize structure in, so it is the closest single "
            "number to 'is this entry a good buy'. Use it, but never alone: "
            "on a top-heavy slate a lineup can carry solid ROI by cashing "
            "often and still have almost no path to first.\n"
            "- **PROJECTED POINTS IS A QUALIFIER, NOT THE HEADLINE** (user "
            "directive 8/29/26: the number one thing you choose on must NOT "
            "be projected points). Scale each slate so its best possible "
            "lineup = 100: across 14 slates the typical contest WINNER "
            "projected 94 and the typical ENTRY projected 94 too. Winners "
            "are not further up the projection scale than the field — they "
            "sit in the same place. So projection tells you a lineup is "
            "strong enough to belong; it does not tell you it can win. Lead "
            "with the chance of finishing first (top1%), and use projection "
            "to check the lineup is not carrying dead weight. Still name "
            "both in the Why — a reader needs to see you checked — but "
            "never argue 'this is the pick because it projects highest'.\n")
        _why_block = (
            "**Why these picks:** <THE MAIN OUTPUT. A cohesive argument, not "
            "a list of numbers (user directive 8/29/26). It must pull FIVE "
            "things together into one read, and it must show how they "
            "connect — a paragraph that mentions all five separately has not "
            "done the job:\n"
            "  1. **Top 1%** — its shot at actually WINNING. This leads the "
            "argument; a tournament pays the top, not the average.\n"
            "  2. **Sim ROI** — what the simulation says the entry is "
            "worth.\n"
            "  3. **Ownership** — how many other teams will look like "
            "this?\n"
            "  4. **Projected points** — a check that the lineup is strong "
            "enough to belong, NOT the reason to pick it (see above).\n"
            "  5. **Slate dynamics** — WHAT YOU THINK THE FIELD IS DOING, "
            "and HOW THIS LINEUP BEATS IT. This one is the spine of the "
            "argument, not a footnote. Say who the crowd is piling onto and "
            "why, then say where this lineup steps away from that crowd and "
            "what has to happen for that step to pay.\n"
            "Where two of them DISAGREE, say so and say which one you "
            "trusted — 'his projection is the third best on the board but "
            "only 8% of teams will have him, and that gap is the whole "
            "reason to take him'. A pick whose numbers all point the same "
            "way is a fine pick; say that plainly too.\n"
            "Length: 6-12 short sentences. Every number gets its plain "
            "meaning in the SAME sentence — '1.9% top1 means about a 1-in-50 "
            "shot at first place', '38% owned means about 4 of every 10 "
            "teams have him', 'ROI of +45% means the sim expects this entry "
            "to return about $1.45 for every $1'. Plain meaning FIRST, the "
            "DFS word in parentheses after — 'picked by few teams "
            "(low-owned)'. Write it so a 5th grader follows the whole "
            "argument start to finish: short sentences, one idea each, no "
            "clause chains. If the pick carries a `cost`, this is also where "
            "you name the player and the rule and defend the override.>\n\n")

    prompt = (
        f"You are PICKING the user's entries for ONE DraftKings contest: \"{sim_label}\" "
        f"(sport: {sport}). Field size {int(sim_contest.get('field_size') or 0):,} entrants · "
        f"${sim_contest.get('entry_fee')} entry · payout shape {shape} · the user is entering "
        f"exactly {my} lineup(s) in this contest.\n\n"
        f"HARD RULE — selection is not construction: every lineup you may pick already "
        f"exists, built {'' if no_sim else 'and simmed '}by the Sim tool, in the candidate table at `{slice_p}`. "
        f"You choose rows BY ID from that table. You NEVER write, edit, combine, or swap "
        f"players. A pick that is not a row in the table will be rejected by the app and "
        f"nothing will be saved.\n\n"
        + (f"HARD RULE — one lineup, one contest: {len(taken)} lineup(s) are already "
           f"picked for this slate's other contests and have been REMOVED from the table "
           f"below. Every contest gets its own lineups; nothing is entered twice.\n\n"
           if taken else "")
        + f"THE SLATE STRATEGY IS A GUIDE, NOT A GATE (user directive 8/29/26). Nothing "
          f"has been filtered out of the table: every lineup in the pool is available to "
          f"you, and each one carries its strategy PRICE in the `cost` column. Here is "
          f"what the strategy asked for and what each rule costs:\n\n{gate_md}\n\n"
          f"So you MAY pick a lineup that breaks a rule — DFS is a game of using data "
          f"against the field, and a strategy written before lock is a strong opinion, not "
          f"a law. But an override is a DECISION you have to defend: if your pick carries "
          f"a `cost`, your **Why** must NAME the player and the rule and say plainly what "
          f"makes the lineup worth that price. A break the why does not mention is "
          f"REJECTED by the app and nothing is saved — not because breaking the rule is "
          f"wrong, but because an unexplained override teaches us nothing, and every "
          f"override is logged and scored against your real finish over the coming "
          f"slates. Default to the strategy; depart from it on purpose, in writing.\n\n"
          f"The strategy also has rules no column can check. Read "
          f"`data/slate_analysis/{slug}.md` IN FULL before you choose, and obey its "
          f"`## Build it like a sharp` steps — the anchor decision, what a sharp "
          f"refuses, the salary shape, and especially its numbered "
          f"**pre-lock check**. (Its leverage step NAMES low-owned candidates; that is "
          f"a menu of plays available to you, never a slot you have to fill.) "
          f"Run that pre-lock check against your pick. A row with better sim numbers that "
          f"fails a pre-lock question normally LOSES to a row that passes it — but this is "
          f"a guide too: if you are convinced the failing row is the better tournament "
          f"play, take it and say why in the Why. **ONE EXCEPTION, and it is "
          f"absolute: ignore any pre-lock question that requires a player for being "
          f"LOW-OWNED** — 'at least one sub-10% player', 'carries a leverage piece', "
          f"'inside the own-per-slot band', or any similar ownership threshold, however "
          f"it is worded and wherever it appears (the strategy doc, a framework file, a "
          f"checklist). That is not a call this slate's strategy made — it is a "
          f"cross-slate average, the pros only do it in ~15% of their lineups, and "
          f"contest winners regularly carry zero low-owned players. Such a question NEVER "
          f"rejects a pick, never breaks a tie, and never outranks a sim number. Answer it "
          f"N/A and move on.\n\n" +
        f"Read, in this order: the candidate table at `{slice_p}` (each row: id, salary, "
        f"projection, average ownership, THIS contest's sim numbers, and the players with "
        f"their ownership); the bundle at `{bundle_path}`; the slate strategy at "
        f"`data/slate_analysis/{slug}.md` and the player pool board at "
        f"`data/player_pool/{slug}.md` when they exist; the strategy docs for sport "
        f"`{sport}`: `rules/{slug}/philosophy.md`, `rules/{slug}/framework.md`, "
        f"`rules/{slug}/autopsies.md`, `rules/{slug}/lessons.yaml` (apply every OPEN "
        f"hypothesis/validated lesson whose mechanism fits; silently drop the rest), "
        f"`rules/shared/anchor_equivalence.md`, `rules/shared/sharp_playbook.md`, and the "
        f"venue file (golf → rules/pga_classic/courses, nascar → rules/nascar/tracks; "
        f"mma has none).\n\n"
        + _metric_block
        + f"- Picking {my} lineup(s) means each pick must earn its own reason. If that is more "
        f"than 1, the picks should win in DIFFERENT ways, not be near-copies.\n"
        f"- A trap is a price, not a player: judge every lineup on THIS slate's numbers.\n"
        f"- The `strategy` column names the low-owned (leverage) players a lineup carries. "
        f"That is INFORMATION, not a score: those names come from an ownership screen "
        f"(under 10% owned), NOT from a decision the slate strategy made. **A lineup that "
        f"carries none of them is not worse, and an empty `strategy` cell is not a flaw.** "
        f"NEVER require a low-owned player in a pick, never prefer a lineup because it has "
        f"one, and never reject one because it doesn't — your own ledger's rule is that the "
        f"pros carry a low-owned piece in about 15% of their lineups, not in every one, and "
        f"contest winners regularly carry zero. Judge every row on THIS slate's strategy and "
        f"its sim numbers.\n"
        f"- A ⚠ (UNDERWEIGHT) entry is different — it IS a cost the strategy named: use that "
        f"player LESS than the crowd, never zero. Pick a ⚠ row only when its sim edge over "
        f"the clean rows is real, and never put the same underweight player in every entry "
        f"of a multi-entry contest — the app rejects that pick.\n\n"
        f"Write `{out_path}` in EXACTLY this format:\n\n"
        f"## Picks — {sim_label}\n\n"
        f"| pick | id | players | why |\n"
        f"|---|---|---|---|\n"
        f"| 1 | <id from the table> | <players copied from that row> | <one short sentence> |\n\n"
        f"(exactly {my} data row(s) — never more, never fewer)\n\n"
        + _why_block
        + f"**Strategy check:** <one line per question in the slate strategy's numbered "
        f"pre-lock check, each answered YES or NO for the pick, quoting the question. "
        f"Answer honestly — a NO is a legal answer, the same guide-not-gate rule as the "
        f"cost column: keep the pick only if your Why already says why it beats the rows "
        f"that pass, and never write YES to a question the lineup actually fails. "
        f"EXCEPT a question requiring a low-owned player (see above): answer it "
        f"'N/A — not a rule' and change nothing about the pick.>\n\n"
        f"Do not add sections. Do not ask questions — read the inputs and produce the file."
    )
    res = _run_claude(prompt, out_path)
    res.update(key=key, sim_label=str(sim_label))
    return res


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
        f"  `**N. Player Name** — $salary, own% (per source), proj X[, ceiling Y]` then a 1–2 "
        f"sentence synthesis in PLAIN, COMPLETE ENGLISH: how it wins (the ceiling path / the edge) "
        f"+ the key risk or condition. Write for a smart 5th grader (user directive 7/27/26), and "
        f"keep it SHORT (8/9/26) — say it once, clearly, and stop. "
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
        f"heads-up that YOUR OPPONENTS pile in — a map of their habit, never a quality read, "
        f"never a fade command, and never a reason to tier the player lower.\n"
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
        f"the picker check at `{hist_dir}/picker_check.json` (if present — per contest, the "
        f"POOL/SLICE/PICK chain: did the Sim build a contest-winning lineup, did it reach the "
        f"table Claude was shown, and where did the pick land), "
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
        f"1c3. TABLE VS PICK (only when `picker_check.json` exists with contests): sim_autopsy's "
        f"pool-vs-picking judges the ENTERED lineups against the pool; this file splits the "
        f"selection step itself. Per contest: `pool_held_winner` (the build), `slice_held_winner` "
        f"(did a winning lineup reach the candidate table Claude was shown — absent means no "
        f"archived table, say so and move on), `pick_pool_pctile` (the share of the pool the pick "
        f"beat), and `n_slice_above_pick` (rows ON the shown table that outscored the pick — the "
        f"8/29 look-DOWN-the-table failure, counted). A pool miss is a BUILD finding, a slice miss "
        f"is a TABLE finding, table rows above the pick is a PICK finding — name which link broke, "
        f"never blame the picker for a lineup it was never shown. A pick at or below the pool's "
        f"median on multiple slates is a recurring picker lesson.\n"
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
        f"4. WRITE `{out_path}` with EXACTLY these sections, in this order, with these word "
        f"budgets (LENGTH BUDGET updated 8/11/26 — specificity beats brevity; the user: 'I "
        f"don't want the strategy and autopsy findings to become too vague': the WHOLE review "
        f"is **at most 1,800 words** — aim for 1,000–1,500; the old 2,500-6,600-word reviews "
        f"stay the failure this replaces, but NEVER VAGUE outranks short: every finding names "
        f"its player and its numbers — 'the day's top scorer sat in Okay' is banned, write "
        f"'Benjamin James ($8,700) — the day's top scorer at 84.25 — sat in Okay'; if cutting "
        f"words would cost a claim its name or number, keep the words):\n"
        f"   - '## What happened' (~150 words) — at most 6 numbered PLAIN sentences anyone could "
        f"follow with zero DFS knowledge: how the user finished, who won the contest and what "
        f"their lineup did differently, and the one thing that decided the slate — every "
        f"deciding player NAMED with salary/score/ownership.\n"
        f"   - '## Process scorecard' (~400 words) — WHY it happened: the findings from steps "
        f"1/1b/1c/1c2/1d above, each finding two or three SPECIFIC sentences carrying its "
        f"player names and numbers (never a vague summary line), each with its what-to-do-next "
        f"attached. Grade the decisions, not the results.\n"
        f"   - '## Lesson ledger changes' (~120 words) — ONE line per lesson touched: what "
        f"changed and the one-line evidence.\n"
        f"   - '## Venue file changes' (~40 words) — the observation appended, in one or two "
        f"lines.\n"
        f"   - '## Ledger hygiene' (~150 words; ONLY if step 1e ran — omit the section when "
        f"there were no flags) — ONE line per decision (RETIRE/KEEP/MERGE + the one-line "
        f"reason).\n"
        f"   - '## Proposed codifications' (~150 words) — for any lesson meeting the promotion "
        f"criteria (3 confirming slates) the exact framework.md/philosophy.md edit you propose; "
        f"for retirement candidates (2 mechanism contradictions) the same. If nothing "
        f"qualifies, write 'None this slate.' under the heading.\n"
        f"   - '## What this means for next slate' (~80 words) — 3-5 numbered single-sentence "
        f"takeaways a 5th grader could follow, most important first.\n"
        f"Do NOT edit framework.md or philosophy.md in this run — proposals only; the user "
        f"approves.\n"
        f"GPP guard: a bad ROI or a lost contest is NEVER a contradiction by itself; only mechanism "
        f"failures count. Do not ask any questions — produce the file.\n\n"
        f"HOW TO WRITE THE REVIEW (user directives 7/27/26 'write for a smart 5th grader' + "
        f"8/9/26 'keep it SHORT — compact, simple, straightforward'):\n"
        f"- Keep the EXACT section headers listed above (the app reads them by name), but under "
        f"every header, START with one plain sentence saying what the section is about. Example "
        f"under '## Process scorecard': 'This section grades HOW you played the slate — the "
        f"decisions, not the results.'\n"
        f"- Short sentences, ordinary words, one fact per sentence (~15 words, hard stop 25). No "
        f"semicolon chains. No more than two numbers in a sentence. Say each thing ONCE — "
        f"repetition across sections is where the old 6,000-word reviews came from.\n"
        f"- DO THE ANALYSIS with the full analyst vocabulary in your head — WRITE the finding the "
        f"way you'd tell a smart 12-year-old what it means. Never print these words bare: "
        f"'structural axis' → 'the main way winning lineups looked different from yours'; "
        f"'own/slot' → 'average ownership per roster spot'; 'Spearman near 0' → 'this pre-lock "
        f"number did not predict the real scores at all'; 'picking_edge_points' → 'how many "
        f"points better picking from the pool would have added'; 'mechanism' → 'the reason it "
        f"works'. The number still appears — the plain meaning carries the sentence.\n"
        f"- Say the plain meaning FIRST and put the DFS or ledger word in parentheses after, EVERY "
        f"time it appears: 'the low-owned player who could decide the slate (the definer)', 'an "
        f"idea we are still testing (a hypothesis lesson)', 'a rule that has proven itself and now "
        f"lives in your framework (codified)', 'whether your entries followed your own plan "
        f"(adherence)'. Never assume a term stuck from an earlier section.\n"
        f"- Explain what every number MEANS: not 'best percentile 3.5' but 'your best entry beat "
        f"96.5% of the field (top 3.5%)'. Not '0 of 2 leverage candidates' but 'the strategy named "
        f"2 low-owned players who could decide the slate, and none of your entries had either one'.\n"
        f"- When you grade something as good or bad, say in one plain sentence WHAT TO DO ABOUT IT "
        f"next slate. A grade without a next step is just a scold."
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
