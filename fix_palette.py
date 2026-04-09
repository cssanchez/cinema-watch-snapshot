with open(".Jules/palette.md", "a") as f:
    f.write("\n## 2026-04-09 - Focus-Visible for Keyboard Navigation\n")
    f.write("**Learning:** Replaced `:focus` pseudo-classes with `:focus-visible` to prevent annoying focus rings on mouse clicks while retaining proper focus rings for keyboard navigation. Additionally, added explicit `:focus-visible` styling for `<a>` tags to ensure full keyboard navigability throughout the interface.\n")
    f.write("**Action:** Use `:focus-visible` instead of `:focus` when styling interactive elements to respect the user's input method. Always ensure `<a>` tags have clear visual indicators when focused.\n")
