# Palette's Journal
## 2024-04-07 - Accessibility Polish\n**Learning:** In a static site generated via Python templates, focus styles for keyboard navigation need to use `:focus-visible` rather than `:focus` to maintain good mouse UX, and language switcher buttons without text labels need `aria-label` attributes.\n**Action:** Replaced `:focus` with `:focus-visible` on interactive elements and added `aria-label` to language toggle buttons across all static HTML files.

- **Date:** 2026-04-08
- **Learning:** Context-setting elements like location selectors perform best when extracted from nested dropdowns into prominent, standalone UI elements (e.g., pill buttons) that clearly dictate the state of the content below them.
- **Action:** Created `move_location_selector.py` script to relocate the zone dropdown from the top navigation bar to a dedicated horizontal block underneath the hero banner, using the pre-existing `.location-selector` CSS class.

## 2026-04-09 - Focus-Visible for Keyboard Navigation
**Learning:** Replaced `:focus` pseudo-classes with `:focus-visible` to prevent annoying focus rings on mouse clicks while retaining proper focus rings for keyboard navigation. Additionally, added explicit `:focus-visible` styling for `<a>` tags to ensure full keyboard navigability throughout the interface.
**Action:** Use `:focus-visible` instead of `:focus` when styling interactive elements to respect the user's input method. Always ensure `<a>` tags have clear visual indicators when focused.
