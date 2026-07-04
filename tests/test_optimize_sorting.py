import pytest
from pathlib import Path
from optimize_sorting import process_file

def test_optimize_sorting_standard(tmp_path):
    html_content = """
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
      }
"""
    file_path = tmp_path / "test.html"
    file_path.write_text(html_content, encoding='utf-8')

    assert process_file(file_path) is True

    new_content = file_path.read_text(encoding='utf-8')

    assert "leftKey.localeCompare(rightKey)" not in new_content
    assert "const lDate = left.date_iso || '';" in new_content
    assert "if (lDate !== rDate) return lDate < rDate ? -1 : 1;" in new_content
    assert "const lTitle = left.movie_title || '';" in new_content
