# DFS Slate Analyzer — Claude Instructions

This repo **analyzes DFS slates**. It does not run Monte Carlo simulations or solve optimization problems. Lineup construction here is done by hand using analysis + the user's framework, not by a solver. For solver-based building, the user has a separate sim repo at `~/Desktop/Repo/ryanjsieb30DFS`.

## Sister repo

The sim repo at `~/Desktop/Repo/ryanjsieb30DFS` is the source of truth for:
- Vendor CSV signature detection (`src/vendors.py` — copied here at scaffold time)
- Original philosophy / framework / autopsies docs (copied here at scaffold time)

When the sim's vendor parsing changes, manually re-copy `src/vendors.py`. When philosophy/framework/autopsies are updated in either repo, mirror to the other.

## Per-slate workflow

Each slate gets its own folder under `slates/`:

```
slates/<YYYY-MM-DD>__<sport>__<slug>/
├── inputs/
│   ├── projections/         # Vendor CSVs (ETR, DailyFan, etc.)
│   ├── salaries/            # DK player pool CSV
│   ├── ownership/           # Own% files
│   ├── contests/            # DK contest entry CSV (what the user is in)
│   └── research/
│       ├── articles/        # PDFs + parallel .txt extracts
│       ├── podcasts/        # Transcripts or notes
│       └── notes/           # User's freeform .md
├── analysis/                # YOU write outputs here
│   ├── landscape.md
│   ├── projections_diff.md
│   ├── build_brief.md
│   └── lineups.csv          # Only if user asks
└── post_slate/
    ├── results.csv
    ├── autopsy.md
    └── autopsy_data.jsonl
```

## The five analysis workflows

| User says | You read | You write |
|---|---|---|
| "Analyze the slate" | ALL of `inputs/projections/`, `ownership/`, `research/articles/`, `research/podcasts/`, `research/notes/`, plus `rules/<sport>/*` | `analysis/landscape.md` — chalk tiers, leverage map, anchor-equivalence check, narrative themes from articles, key questions for the slate |
| "Where do vendors disagree?" | All vendor CSVs in `inputs/projections/` | `analysis/projections_diff.md` — players where vendors materially diverge, with implication for ownership/leverage |
| "Tell me about <player>" | Everything | Inline reply (write a file only if user asks) |
| "How should I build for <contest>?" | Everything + `inputs/contests/` | `analysis/build_brief.md` — anchor recommendations, leverage spots, anchor-equivalence requirements, thesis themes per lineup slot |
| "Log the autopsy" | `post_slate/results.csv` + saved analysis | `post_slate/autopsy.md` + `post_slate/autopsy_data.jsonl`; append to `rules/<sport>/autopsies.md`; mirror lesson into sim repo's `rules/<sport>/autopsies.md` |

## Hard rules (mirrors user memory)

- **No scraping.** Inputs are paste/drop only.
- **GPP-only framing.** Optimize for ceiling/leverage/contrarian, never cash.
- **Before any slate-strategy answer**: auto-read `inputs/research/` + `rules/<sport>/philosophy.md` + `framework.md` + `autopsies.md` + active projections.
- **Anchor-Equivalence Rule** (`rules/shared/anchor_equivalence.md`): if 2+ chalk-tier anchors at similar own, ≥1 lineup MUST run the alternative. Mandatory pre-lock check on every build brief.
- **NASCAR**: before any NASCAR analysis, read `rules/nascar/tracks/<track-slug>.md`. If missing, ask the user for a track description.
- **PGA RD4 SD**: flat 6-golfer lineup, **NO captain, NO 1.5x**. Never reference "CPT" for this contest type.
- **No stddev required.** Vendors don't ship it; loader derives from ceiling or defaults to 30% of proj.
- **Thesis required**: every recommended lineup needs a one-sentence "how it wins" thesis.
- **No competing lineups**: lineups in a portfolio must answer DIFFERENT "what if?" questions.
- **Sim rank ≠ gospel**: build for the tail (winning), not the expected case.
- **Never commit without explicit instruction.** "done"/"next"/"looks good" are NOT commit triggers.

## Post-autopsy ritual

After writing an autopsy, auto-read `post_slate/autopsy_data.jsonl` + the slate's analysis files, surface 2-3 paragraphs of lessons, then ask the user whether to codify into `rules/<sport>/philosophy.md` or `framework.md`. Don't wait to be prompted.

## What this repo does NOT do

- No Streamlit UI (Claude-driven only)
- No Monte Carlo simulation
- No automated lineup optimization (hand-built only, on request)
- No YAML rules enforcement (`rules/<sport>/rules.yaml` exists in the sim, not here)
