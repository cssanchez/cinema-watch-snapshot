import pytest
from optimize_sort_rows import process_file

def test_process_file_updates_sort(tmp_path):
    # Setup
    test_file = tmp_path / "test.html"
    original_html = """      function sortRowsForFront(rows, resultPreset = null) {
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
    test_file.write_text(original_html, encoding="utf-8")

    # Execute
    result = process_file(test_file)

    # Assert
    assert result is True
    content = test_file.read_text(encoding="utf-8")
    assert "⚡ Bolt Optimization" in content
    assert "leftKey.localeCompare(" not in content
    assert "lTime < rTime" in content
