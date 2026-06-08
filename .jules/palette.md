## 2024-08-01 - Add aria-live for dynamic results
**Learning:** Screen readers do not announce content injected via Javascript unless the container explicitly has `aria-live` indicating it should be read. For dynamic search/filter result containers, omitting this breaks accessibility.
**Action:** When creating or modifying dynamic client-side result lists or their corresponding empty states, ensure the container includes `aria-live="polite"` and `role="status"`.
