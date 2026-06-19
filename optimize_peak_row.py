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


ORIGINAL_TOP_VENUE = """        // ⚡ Bolt Optimization: Replaced O(N log N) sorting with O(N) reduction to find the top venue
        if (venueBuckets.size) {
          const bucketKey = Array.from(venueBuckets.keys()).reduce((best, current) => {
            const bestCount = venueBuckets.get(best) || 0;
            const currentCount = venueBuckets.get(current) || 0;
            if (currentCount !== bestCount) {
              return currentCount > bestCount ? current : best;
            }
            return current.localeCompare(best) < 0 ? current : best;
          });"""

OPTIMIZED_TOP_VENUE = """        // ⚡ Bolt Optimization: Replaced O(N log N) sorting with O(N) reduction to find the top venue
        if (venueBuckets.size) {
          let bucketKey = null;
          let bestCount = -1;
          for (const [current, currentCount] of venueBuckets.entries()) {
            if (bucketKey === null || currentCount !== bestCount) {
              if (bucketKey === null || currentCount > bestCount) {
                bucketKey = current;
                bestCount = currentCount;
              }
            } else if (current.localeCompare(bucketKey) < 0) {
              bucketKey = current;
              bestCount = currentCount;
            }
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
        changed = False
        if ORIGINAL_PEAK_ROW in content:
            content = content.replace(ORIGINAL_PEAK_ROW, OPTIMIZED_PEAK_ROW)
            changed = True
        if ORIGINAL_TOP_VENUE in content:
            content = content.replace(ORIGINAL_TOP_VENUE, OPTIMIZED_TOP_VENUE)
            changed = True

        if changed:
            file_path.write_text(content, encoding="utf-8")
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
