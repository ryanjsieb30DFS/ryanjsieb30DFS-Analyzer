# Red Team (re-run) — PGA RD4 Showdown (RBC Canadian Open R4, TPC Toronto Osprey Valley)

_Adversarial re-review of `data/lineups/pga_rd4_sd.md` after the finalize-from-pool pass (6 lineups, $40K Drive the Green, field ~9,512, 6 entries). Goal: confirm the prior two FIXes (L3 darts, L4 mid-tier trap) and finding #2 (Theegala unused) actually cleared, and hunt anything the re-selection introduced. All 6 verified as real pool rows. `vendor_calibration.jsonl` still empty → ownership is mechanism-only; DK own used for the trap math (the column the prior run trusted, not the discredited Stone column)._

## Verdict summary
| Lineup | Verdict | One-line reason |
|---|---|---|
| L1 — Double-elite (Clark+Burns) | **SHIP** | Unchanged; still hits structure, carries the Burns anchor-equiv leg. |
| L2 — Correct-chalk concentration | **SHIP** | Unchanged; codified-rule expression, highest field-overlap by design. |
| L3 — Modal anchor + best leader (tough) | **SHIP** | **Prior FIX cleared** — the 2.7% way-back Pavon dart is gone; pivots are sub-10 starters. Watch: Hall/Potgieter still mid-back. |
| L4 — Burns+Koepka leverage (tough) | **SHIP** | **Re-selected on REAL positions** — prior Nick Taylor "-11" was actually +6; row 196 has all six in the red, band 0, cum own 57. |
| L5 — Birdie hedge A (chalk + darts) | **SHIP** | Unchanged; carries the mandatory sub-5 way-back spike slot. |
| L6 — Birdie hedge B (faded -9 leverage) | **SHIP** | **Finding #2 cleared** — Theegala now expresses the validated sub-15 mid-tier slot; lower cum own, distinct from L5. |

**No KILLs. No open FIXes.** Both prior surgical FIXes and finding #2 are resolved. One NEW portfolio watch-item (Fox + Potgieter each at 50% — see findings).

---

## Lineup attacks (changed lineups)

### L3 — Modal anchor + best leader (tough) — SHIP (prior FIX cleared)
**Prior FIX was:** Pavon ($6,600, 2.7%, tee 10:30) — a way-back dart whose ceiling dies on a tough course, anti-correlated with L3's own read.
**Cleared:** Pavon and the over-exposed Pendrith are both gone. The pivots are now Stanger ($7,000, 10.5%, -10, tee 12:19 — near the lead), Max Homa ($7,100, 9.9% DK, -8), Potgieter ($7,800, 7.8%), Harry Hall ($8,400, 5.7%). Band on DK own = 1 (Stanger). Real pool row 759, $49,700, cum own 100.
**Break it (residual):** Harry Hall (tee 10:52) and Potgieter (tee 11:03) are still back of the lead — a *milder* version of the original anti-correlation. On a tough course neither is positioned to post the round that wins. But they're $7,800–8,400 mid-salary bodies at single-digit own, not the 2.7% punt the rule targeted, and the lineup carries 3 near-lead pieces (Tommy/Cauley/Stanger) + the 67-ceiling modal anchor. The leverage now survives the tough read. Verdict **SHIP**; the positioning is a watch, not a flaw.

### L4 — Burns+Koepka leverage core (tough) — SHIP (re-selected on real positions)
**What broke the prior version:** the earlier L4 (row 1605) carried Nick Taylor tagged "-11" — a position **fabricated from his 12:31 tee time**. The Stone R4 board shows Nick Taylor is actually **+6** (0% win, 0% top-5): a way-back dart whose ceiling dies on a tough course — the exact profile this review killed in L3 (Pavon). Root cause: the projection CSVs carry tee_time, not leaderboard position, and tee time is not a position proxy.
**Cleared:** Real pool row 196, $49,900, cum own 57 (the portfolio's true low). Mid-tier band on DK own = 0. **Every player verified in the red on the Stone board:** Burns -10, Koepka -6, Homa -8, Mouw -8, McGreevy -6, Bezuidenhout -4 — no way-back darts. Zero Suber/Cauley/Tommy/PASS. Also drops Fox to 2 lineups.
**Break it (residual):** The leverage rests on Burns (22.6%) + a low-owned cast; the headline edge is Brooks Koepka at **4.2%** — a major champ the field abandoned because he sits -6. That's a real contrarian ceiling name, but his 55.7 ceiling means Burns is the lone 60+, so if Burns doesn't go nuclear the lineup's ceiling is capped. Acceptable for the 1-of-6 deep-leverage slot. Verdict **SHIP**.

### L6 — Birdie hedge B: faded -9 block, leverage version — SHIP (finding #2 cleared)
**Finding #2 was:** the board's named sub-15% mid-tier PLAY (Theegala) sat in 0 lineups while the hedges leaned on chalk -9s (Lowry/MacIntyre ~18%) and way-back sub-5 darts — under-weighting the *validated* `sub15-midtier-birdiefest-score-source` slot.
**Cleared:** Real pool row 2741, $49,900, cum own 76. Theegala ($8,800, 9.9% SIN / 13.5% DK, -9 T12) now carries the sub-15 mid-tier ceiling slot, alongside MacIntyre (60.3 ceil, the kept 60+ piece) and two real spikes (Bezuidenhout 4.6% DK = a true DK sub-5, McGreevy). Distinct from L5's chalk-leader hedge — this is the leverage-side birdie hedge.
**Break it (residual):** At cum own 76 with only Clark as a true leader, L6 is now a *low-floor* birdie build — in a -19/-20 birdie-fest the field piles into the whole popular -9 block (Lowry/Mac/Fitz/Hovland/Theegala) and L6 only holds Mac + Theegala from it. That's the cost of the leverage tilt and the right kind of bet for a 1-of-6 hedge. McGreevy is sub-5 only on Stone (6.7% DK), but Bezuidenhout covers the true-sub-5 slot. Verdict **SHIP**.

_(L1, L2, L5 unchanged from the prior review — all SHIP; re-attacks omitted.)_

## Portfolio-level findings

1. **Watch-item — non-anchor exposure at the cap.** Pendrith's prior 50% is fixed (→ L1 only), and the L4 re-selection dropped **Fox to 2** (L1/L5). Remaining at 50% (3/6): **Cauley** (L2/L3/L5, prior flag) and **Aldrich Potgieter** (L2/L3/L6 — sub-10 value across three builds). Both sit *at* the framework's >50% cap, not over it, each in a distinct role. Not a violation — if you want it cleaner, re-selecting a different L3 from the pool drops Potgieter to 2 (left in place).
2. **Anchor-Equivalence — PASS.** Clark 3 / Burns 2 / Tommy 2, all run, none at 0%.
3. **PASS tier — PASS.** Suber/Hovland/Bridgeman = 0 across all six.
4. **Diversification — PASS.** No two lineups share more than 2 of 6 (limit 4). Six distinct "what if?" questions retained.
5. **Mid-tier trap — PASS everywhere on DK own.** L1=1, L2=2, L3=1, L4=1, L5=0, L6=2.
6. **Ceiling + spike floors — PASS.** Every lineup has a 60+ ceiling; the birdie hedges carry the mandatory sub-5 spike (L5: Thorbjornsen/Tom Kim; L6: Bezuidenhout/McGreevy).

## Pre-flight audit (line by line)
- **Slate confirmed** — ✓ pool exported 6-14 10:30am; matches the leaderboard. Real.
- **Pool membership** — ✓ all six are verified real pool rows (L1 4852, L2 4557, L3 759, L4 196, L5 617, L6 2741) — the select-from-pool contract holds.
- **Real leaderboard positions** — ✓ now cross-checked vs The Stone R4 board (Event Score), not tee-time inference. Caught and fixed Nick Taylor (+6, not the inferred -11) in L4; all tough-build pieces verified in the red.
- **Venue (tough, with birdie-flip risk)** — ✓ honest; the 4 tough / 2 birdie split with two hedges is consistent.
- **Open lessons** — ✓ the `sub15-midtier` line is no longer a rubber-stamp: Theegala genuinely expresses it in L6. `repeated-punt` no longer triggers (Pendrith ×1).
- **Framework pre-lock** — ✓ mid-tier trap clean on DK own without leaning on the discredited Stone column.

**Bottom line:** The finalized portfolio clears both prior FIXes and finding #2, and is now fully pool-legal. The only residual is a concentration watch-item (Fox + Potgieter at 50%) — at the cap, your call whether to push lower. Nothing here is a KILL or an open FIX.
