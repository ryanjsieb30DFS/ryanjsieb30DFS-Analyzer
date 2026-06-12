# MLB Classic — Framework

> **STRATEGY TO BE PROVIDED.** Only the factual roster/contest rules are filled in below.
> The user will supply the operational playbook (stack-size rules, secondary-stack logic,
> pitcher selection, exposure caps, pre-lock checklist). Until then, build using these facts
> plus general MLB GPP principles, and note that the framework is not yet fully codified.

## Roster & contest facts (DK MLB Classic)

- **Roster: 10 players** — `P, P, C, 1B, 2B, 3B, SS, OF, OF, OF` (2 pitchers + 8 hitters).
- **Salary cap: $50,000.**
- **Scoring is correlation-driven**: hitters on the same team score together when the offense
  goes off — this is why **team stacking is the core construction lever** (not isolated value).
- **Never roster a hitter against your own pitcher.**
- A valid lineup must fill every position slot; OF needs 3, one each of C/1B/2B/3B/SS, exactly 2 P.

## Construction (codified from the lesson ledger)

- **Pivot budget — small-field SE (≤~1,200 entries):** build chalk-plus-ONE-structural-pivot:
  ~15–18% average ownership, roughly 3–5 sub-10% plays, one leverage axis (stack OR pitcher —
  never both). Layered contrarianism out-leverages the field and trades ceiling for uniqueness
  nobody is contesting. *(Codified 2026-06-12; 3 mechanism confirmations: 6/9, 6/10, 6/11 —
  incl. the 6/11 same-slate contrast where the in-band build hit top 4.4% and the above-band
  build finished mid-pack. Ledger: mlb-classic-2026-06-10-pivot-budget-small-field-se.)*
- **Salary-enabler pitcher chalk:** a cheap chalk arm whose salary unlocks the winning bat
  structure is an enabler, not a chalk trap — keep it; fading it is a structural decision that
  cuts you off from the winning salary shape, not a leverage play. A short leash (low avg IP)
  is a **risk note, not a fade trigger** — leash-based fades went 1-1 (Teng busted 6/9,
  Phillips smashed 6/11). *(Codified 2026-06-12; enabler-keep 3-for-3: May, Detmers, the
  Phillips fade cost. Ledger: mlb-classic-2026-06-10-salary-enabler-pitcher-chalk.)*
- **Coors games:** read `parks/coors_field.md` — the repeatable equity is the **cheap
  unowned-side one-off**, never the consensus stack or the owned name (3-for-3: Castro 6/9,
  Carrigg 6/10 + 6/11; owned pieces failed to pay all three slates).

_Still to be detailed by the user: primary stack size rules, secondary/mini-stack logic,
pitcher pairing, batting-order requirements, exposure caps._

## Lineup discipline (inherited, applies now)

- Each lineup needs a one-sentence thesis ("how it wins").
- Lineups in a portfolio must answer DIFFERENT questions — distinct stacks/game-environments,
  not the same stack reshuffled.
- Apply the shared Anchor-Equivalence pre-lock check.
- Verify total salary ≤ $50,000.
- **HARD RULE — tracked entries only:** every lineup entered on DK must exist in
  `data/lineups/mlb_classic.md` before lock (Claude-built, handbuilt, or chat-built with a
  logged thesis). An untracked entry bypasses the thesis requirement, the red team, and the
  portfolio audit, and the autopsy then grades a portfolio that wasn't played. *(Codified
  2026-06-12; 3 slates of evidence in both directions. Ledger:
  mlb-classic-2026-06-10-untracked-entry-bypasses-loop.)*
