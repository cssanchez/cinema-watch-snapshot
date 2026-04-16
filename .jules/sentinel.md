## 2025-04-07 - [Added Content-Security-Policy (CSP)]
**Vulnerability:** Missing Content-Security-Policy (CSP) headers or meta tags across the static application.
**Learning:** The static website hosted on GitHub Pages did not define a Content-Security-Policy. Although no immediately exploitable Cross-Site Scripting (XSS) vulnerability was found, defense-in-depth is critical for mitigating the impact of future script injection flaws, especially in a client-heavy application relying on URL parameters and innerHTML.
**Prevention:** Apply a strict Content-Security-Policy using `<meta http-equiv="Content-Security-Policy">` restricting scripts and resources to the same origin (`'self'`) to protect the static site.

## 2026-04-08 - [Fixed Catastrophic Backtracking (ReDoS)]
**Vulnerability:** Regular Expression Denial of Service (ReDoS) in `apply_ux_improvements.py`.
**Learning:** Nested quantifiers on overlapping character groups (e.g., `(?:<[^/][^>]*>(?:[^<]|<[^d][^>]*>)*)*`) can lead to exponential backtracking when processing malicious or long input strings.
**Prevention:** Avoid nested quantifiers and use non-greedy matches (`.*?`) or dedicated HTML parsers to process complex document structures safely.
## 2024-04-08 - [Content Security Policy in Static Sites]
**Vulnerability:** Missing Content-Security-Policy (CSP) headers leaving the static site vulnerable to XSS and data injection attacks.
**Learning:** For a statically exported site hosted on GitHub Pages, server HTTP headers cannot be configured directly. Therefore, the CSP must be implemented via HTML `<meta http-equiv="Content-Security-Policy" content="...">` tags injected into the `<head>` of every generated static HTML file.
**Prevention:** Include a build step or post-processing script that automatically injects a strict CSP meta tag into all generated `.html` files before deploying to GitHub Pages.

## 2025-04-15 - [Prevented DOM-based XSS with URL Protocol Sanitization]
**Vulnerability:** DOM-based Cross-Site Scripting (XSS) via unvalidated `href` injection.
**Learning:** The static frontend dynamically constructed and injected anchor tags (`<a>`) using URL values from JSON (e.g., `item.movie_href` and `item.venue_href`). Although `escapeHtml` was used, it does not prevent malicious URI schemes like `javascript:`, `data:`, or `vbscript:` from executing scripts when a user clicks the injected link.
**Prevention:** Implement explicit protocol sanitization logic to reject dangerous schemes (e.g., setting the result to `#`) before encoding and injecting URL attributes into the DOM.
