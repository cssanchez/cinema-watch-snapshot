#!/usr/bin/env python3
"""
Performance optimization script to replace O(N log N) sorting with O(N) reduction when finding the peak screening row.
"""
import pathlib
import sys

DOCS_ROOT = pathlib.Path(__file__).parent / 'docs'

ORIGINAL_PEAK_ROW = """        let peakRow = null;
        if (soldRows.length) {
          peakRow = [...soldRows].sort((left, right) => {
            if ((right.sold_percent || 0) !== (left.sold_percent || 0)) {
              return (right.sold_percent || 0) - (left.sold_percent || 0);
            }
            const leftKey = `${left.date_iso}|${left.time_label}|${left.movie_title}`;
            const rightKey = `${right.date_iso}|${right.time_label}|${right.movie_title}`;
            return leftKey.localeCompare(rightKey);
          })[0];
        }"""

OPTIMIZED_PEAK_ROW = """        // ⚡ Bolt Optimization: Replaced O(N log N) sorting with O(N) reduction to find the peak row
        let peakRow = null;
        if (soldRows.length) {
          peakRow = soldRows.reduce((max, current) => {
            const maxSold = max.sold_percent || 0;
            const currentSold = current.sold_percent || 0;
            if (currentSold !== maxSold) {
              return currentSold > maxSold ? current : max;
            }
            const maxKey = `${max.date_iso}|${max.time_label}|${max.movie_title}`;
            const currentKey = `${current.date_iso}|${current.time_label}|${current.movie_title}`;
            return currentKey.localeCompare(maxKey) < 0 ? current : max;
          });
        }"""

def process_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
        if ORIGINAL_PEAK_ROW in content:
            new_content = content.replace(ORIGINAL_PEAK_ROW, OPTIMIZED_PEAK_ROW)
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
            print(f"Patched: {file_path.relative_to(DOCS_ROOT)}")

    print(f"Done! Patched {patched} out of {len(html_files)} HTML files.")

if __name__ == "__main__":
    main()
