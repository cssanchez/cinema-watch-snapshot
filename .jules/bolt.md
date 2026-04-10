## 2025-04-08 - [String Normalization Memoization]
**Learning:** In the frontend static site (`cinema-watch-snapshot`), string normalization and regex functions (e.g., `foldText`, `canonicalLanguage`, `normalizeSource`, `canonicalFormat`) are called extensively during client-side filtering and translation mapping, leading to O(N) redundant calculations on large datasets.
**Action:** Memoize these functions using `Map` to avoid redundant overhead during rendering/filtering. Since the site is statically generated and uses Vanilla JS without a build step in this repository, the optimization is applied via a python patch script.

## 2024-04-08 - [Pre-compiling Regex in processing loops]
**Learning:** In Python scripts that iteratively process many files (like `apply_ux_improvements.py`), using inline `re.compile()` or inline `re.sub()`/`re.search()` causes the regex engine to re-compile (or check its cache for) the pattern on every call, leading to measurable overhead.
**Action:** Always pre-compile regex patterns at the module level using `re.compile()` and reuse them as constants within the file processing loops to eliminate redundant compilation overhead.
## 2025-04-10 - [String Normalization Memoization]
**Learning:** In the frontend static site, string normalization and regex functions used during client-side filtering and translation mapping are called repeatedly on the same data. Since the site is statically generated, we can memoize these pure functions to avoid redundant regex operations. The memory limit size constraint (e.g., `cache.size > 2000`) prevents OOM issues.
**Action:** Memoized pure string manipulation functions with `Map` and size caps to ensure bounded memory usage while skipping repeated O(N) calculations.
