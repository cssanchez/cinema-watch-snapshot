## 2024-04-08 - [Content Security Policy in Static Sites]
**Vulnerability:** Missing Content-Security-Policy (CSP) headers leaving the static site vulnerable to XSS and data injection attacks.
**Learning:** For a statically exported site hosted on GitHub Pages, server HTTP headers cannot be configured directly. Therefore, the CSP must be implemented via HTML `<meta http-equiv="Content-Security-Policy" content="...">` tags injected into the `<head>` of every generated static HTML file.
**Prevention:** Include a build step or post-processing script that automatically injects a strict CSP meta tag into all generated `.html` files before deploying to GitHub Pages.
