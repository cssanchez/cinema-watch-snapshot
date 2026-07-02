## 2026-07-02 - Screen Reader Announcements for Dynamic Content
**Learning:** When implementing asynchronous UI updates (like filtering results) in a static site without full page reloads, screen readers will remain silent unless explicitly instructed otherwise.
**Action:** Add `aria-live="polite"` and `role="status"` to dynamic result containers and empty state messages so screen readers automatically announce when the content changes.
