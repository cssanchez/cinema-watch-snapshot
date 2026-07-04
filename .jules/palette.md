## 2025-02-15 - Dynamic DOM updates require ARIA live regions
**Learning:** When client-side JavaScript filters elements and renders an "Empty State" directly into the DOM (e.g. innerHTML updates), screen readers do not automatically announce the change. Adding `aria-live="polite"` and `role="status"` on the injected empty state container or its parent ensures users relying on assistive technology are notified when no results match their query.
**Action:** Always verify that async DOM changes representing state (like search results or empty states) are wrapped in appropriate live regions.
