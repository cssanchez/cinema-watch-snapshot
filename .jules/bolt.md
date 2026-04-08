## 2026-04-07 - [Hoist Loop-Invariant Normalization]
**Learning:** Found a performance bottleneck where string normalization (using `.normalize('NFD')` and regex replacement) was being performed on the same static filter string (`filters.movie`) inside a loop executing over 2700+ times.
**Action:** Computed `foldText(filters.movie)` once before iterating, drastically reducing redundant operations.
## 2026-04-08 - [Avoid Redundant DOM Traversals in Injected Scripts]
**Learning:** Found a performance bottleneck where injected JS on static pages was querying the DOM (`querySelectorAll`) and rebuilding a `Set` of available locations on *every* call to `setHomepageLocation()`.
**Action:** Memoized the `buttons`, `panels`, and `availableKeys` in module-level variables (within the script scope), reducing the function's execution time significantly (~19ms to ~8ms in benchmarks) by ensuring heavy DOM operations and Set instantiations happen only once.
