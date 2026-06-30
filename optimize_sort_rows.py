#!/usr/bin/env python3
"""
Performance optimization script to eliminate O(N log N) GC pressure in `sortRowsForFront`
by replacing string template concatenations and `.localeCompare()` with pure falsy-fallback
sequential string inequalities.
"""
import pathlib
import sys

DOCS_ROOT = pathlib.Path(__file__).parent / 'docs'

ORIGINAL_SORT = """      function sortRowsForFront(rows, resultPreset = null) {
        const normalizedSort = String(resultPreset?.sort || '').trim().toLowerCase();
        const nextRows = [...rows];
        if (normalizedSort === 'sold_desc') {
          nextRows.sort((left, right) => {
            const leftSold = toInt(left.sold_percent);
            const rightSold = toInt(right.sold_percent);
            const leftRank = leftSold === null ? -1 : leftSold;
            const rightRank = rightSold === null ? -1 : rightSold;
            if (rightRank !== leftRank) {
              return rightRank - leftRank;
            }
            const leftKey = `${left.date_iso}|${left.time_label}|${left.movie_title}`;
            const rightKey = `${right.date_iso}|${right.time_label}|${right.movie_title}`;
            return leftKey.localeCompare(rightKey);
          });
          return nextRows;
        }
        nextRows.sort((left, right) => {
          const leftKey = `${left.date_iso}|${left.time_label}`;
          const rightKey = `${right.date_iso}|${right.time_label}`;
          return leftKey.localeCompare(rightKey);
        });
        return nextRows;
      }"""

OPTIMIZED_SORT = """      // ⚡ Bolt Optimization: Replace GC-heavy string concatenations and localeCompare with pure sequential string inequalities and falsy fallbacks.
      function sortRowsForFront(rows, resultPreset = null) {
        const normalizedSort = String(resultPreset?.sort || '').trim().toLowerCase();
        const nextRows = [...rows];
        if (normalizedSort === 'sold_desc') {
          nextRows.sort((left, right) => {
            const leftSold = toInt(left.sold_percent);
            const rightSold = toInt(right.sold_percent);
            const leftRank = leftSold === null ? -1 : leftSold;
            const rightRank = rightSold === null ? -1 : rightSold;
            if (rightRank !== leftRank) {
              return rightRank - leftRank;
            }
            const lDate = left.date_iso || '';
            const rDate = right.date_iso || '';
            if (lDate !== rDate) return lDate < rDate ? -1 : 1;

            const lTime = left.time_label || '';
            const rTime = right.time_label || '';
            if (lTime !== rTime) return lTime < rTime ? -1 : 1;

            const lTitle = left.movie_title || '';
            const rTitle = right.movie_title || '';
            if (lTitle !== rTitle) return lTitle < rTitle ? -1 : 1;

            return 0;
          });
          return nextRows;
        }
        nextRows.sort((left, right) => {
          const lDate = left.date_iso || '';
          const rDate = right.date_iso || '';
          if (lDate !== rDate) return lDate < rDate ? -1 : 1;

          const lTime = left.time_label || '';
          const rTime = right.time_label || '';
          if (lTime !== rTime) return lTime < rTime ? -1 : 1;

          return 0;
        });
        return nextRows;
      }"""

def process_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
        if ORIGINAL_SORT in content:
            new_content = content.replace(ORIGINAL_SORT, OPTIMIZED_SORT)
            file_path.write_text(new_content, encoding="utf-8")
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

def main():
    if not DOCS_ROOT.exists() or not DOCS_ROOT.is_dir():
        print(f"Error: {DOCS_ROOT} is not a valid directory.")
        sys.exit(1)

    html_files = list(DOCS_ROOT.rglob("*.html"))
    patched = 0

    for file_path in html_files:
        if process_file(file_path):
            patched += 1

    print(f"Done! Patched {patched} out of {len(html_files)} HTML files.")

if __name__ == "__main__":
    main()
