## 2026-04-07 - [Hoist Loop-Invariant Normalization]
**Learning:** Found a performance bottleneck where string normalization (using `.normalize('NFD')` and regex replacement) was being performed on the same static filter string (`filters.movie`) inside a loop executing over 2700+ times.
**Action:** Computed `foldText(filters.movie)` once before iterating, drastically reducing redundant operations.
