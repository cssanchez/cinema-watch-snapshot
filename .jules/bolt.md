## 2025-04-08 - [String Normalization Memoization]
**Learning:** In the frontend static site (`cinema-watch-snapshot`), string normalization and regex functions (e.g., `foldText`, `canonicalLanguage`, `normalizeSource`, `canonicalFormat`) are called extensively during client-side filtering and translation mapping, leading to O(N) redundant calculations on large datasets.
**Action:** Memoize these functions using `Map` to avoid redundant overhead during rendering/filtering. Since the site is statically generated and uses Vanilla JS without a build step in this repository, the optimization is applied via a python patch script.

## 2024-04-08 - [Pre-compiling Regex in processing loops]
**Learning:** In Python scripts that iteratively process many files (like `apply_ux_improvements.py`), using inline `re.compile()` or inline `re.sub()`/`re.search()` causes the regex engine to re-compile (or check its cache for) the pattern on every call, leading to measurable overhead.
**Action:** Always pre-compile regex patterns at the module level using `re.compile()` and reuse them as constants within the file processing loops to eliminate redundant compilation overhead.

## 2024-04-10 - [DOM Query Memoization Formatting]
**Learning:** When using Python to inject javascript block caching variables into an HTML template via regex `lambda` replacements, using multi-line string block literals (e.g., `"""`) can introduce unexpected whitespace, indentation, or blank-line artifacts in the generated HTML due to Python's handling of indentations within the raw block. Furthermore, using global `content.replace()` after injecting definitions can easily introduce infinite recursion bugs by accidentally string-replacing inside the newly injected code block itself.
**Action:** When injecting multi-line code via regex replacements, use explicit concatenation or strictly formatted f-strings with explicit `\n` characters to ensure exact formatting. Crucially, always perform global string replacements on existing code (to apply the cache) *before* injecting the actual new function definition block, to prevent accidental self-mutations.
