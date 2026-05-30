# NASCAR Track References

Per-track markdown files cataloguing physical profile + comparable tracks. Used to provide cross-slate context when reviewing or planning a NASCAR slate.

## Convention

- One `.md` file per track, named `<track_slug>.md` (e.g. `charlotte_motor_speedway.md`)
- Track data is **user-provided** as text — saved here as a cumulative knowledge base
- Each file has: physical profile (length, surface, banking, shape, tire wear), direct comparables, adjacent comparables, strategic notes (accumulates over time)

## Adding a new track

When a NASCAR slate features a track not yet in this directory, ask the user for the description before doing strategy work. See `feedback-nascar-track-reference` memory for the standing rule.

## Future schema

Once 3+ tracks accumulate here, this may migrate to a structured `tracks.yaml` so cross-slate analytics can programmatically filter "show me past performance at intermediate tracks" — but until then, the markdown is sufficient for human + Claude reference.
