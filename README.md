# DFS Slate Analyzer

Claude-driven DFS slate analysis tool. Sister to the sim at `~/Desktop/Repo/ryanjsieb30DFS`.

## How to use

1. Create a slate folder: `slates/<YYYY-MM-DD>__<sport>__<slug>/`
2. Drop vendor files into `inputs/`:
   - Projections CSVs → `inputs/projections/`
   - DK salaries → `inputs/salaries/`
   - Ownership → `inputs/ownership/`
   - DK contest entries → `inputs/contests/`
   - Articles/podcasts/notes → `inputs/research/{articles,podcasts,notes}/`
3. Open Claude Code in this repo and ask:
   - "Analyze the slate"
   - "Where do vendors disagree?"
   - "Tell me about <player>"
   - "How should I build for <contest>?"
   - "Log the autopsy" (after dropping `post_slate/results.csv`)

See `CLAUDE.md` for the full workflow.
