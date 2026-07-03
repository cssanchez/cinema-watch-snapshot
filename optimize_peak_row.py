#!/usr/bin/env python3
"""
Performance optimization script to replace O(N log N) sorting with O(N) reduction when finding the peak screening row.
"""
import pathlib
import sys
import re

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
            const md = max.date_iso || '';
            const cd = current.date_iso || '';
            if (cd !== md) return cd < md ? current : max;
            const mt = max.time_label || '';
            const ct = current.time_label || '';
            if (ct !== mt) return ct < mt ? current : max;
            const mm = max.movie_title || '';
            const cm = current.movie_title || '';
            if (cm !== mm) return cm < mm ? current : max;
            return max;
          });
        }"""

def process_file(file_path):
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        if ORIGINAL_PEAK_ROW in content:
            content = content.replace(ORIGINAL_PEAK_ROW, OPTIMIZED_PEAK_ROW)

        pattern_peak_row = re.compile(
            r"([ \t]*)const maxKey = `\$\{max\.date_iso\}\|\$\{max\.time_label\}\|\$\{max\.movie_title\}`;?\s*"
            r"const currentKey = `\$\{current\.date_iso\}\|\$\{current\.time_label\}\|\$\{current\.movie_title\}`;?\s*"
            r"return currentKey\.localeCompare\(maxKey\) < 0 \? current : max;?",
            re.MULTILINE
        )

        def repl_peak_row(match):
            indent = match.group(1)
            return (
                f"{indent}const md = max.date_iso || '';\n"
                f"{indent}const cd = current.date_iso || '';\n"
                f"{indent}if (cd !== md) return cd < md ? current : max;\n"
                f"{indent}const mt = max.time_label || '';\n"
                f"{indent}const ct = current.time_label || '';\n"
                f"{indent}if (ct !== mt) return ct < mt ? current : max;\n"
                f"{indent}const mm = max.movie_title || '';\n"
                f"{indent}const cm = current.movie_title || '';\n"
                f"{indent}if (cm !== mm) return cm < mm ? current : max;\n"
                f"{indent}return max;"
            )

        content = pattern_peak_row.sub(repl_peak_row, content)

        pattern_top_venue = re.compile(
            r"([ \t]*)return current\.localeCompare\(best\) < 0 \? current : best;?",
            re.MULTILINE
        )

        def repl_top_venue(match):
            indent = match.group(1)
            return f"{indent}return current < best ? current : best;"

        content = pattern_top_venue.sub(repl_top_venue, content)

        if content != original_content:
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
