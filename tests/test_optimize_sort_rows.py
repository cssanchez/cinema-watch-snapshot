import pytest
from optimize_sort_rows import process_file

def test_process_file_applies_optimization(tmp_path):
    f = tmp_path / "index.html"
    f.write_text("""      function sortRowsForFront(rows, resultPreset = null) {
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
      }""", encoding="utf-8")

    assert process_file(f) == True
    content = f.read_text(encoding="utf-8")
    assert "WeakMap" in content
    assert "localeCompare(rightKey);" in content
    assert "const leftKey =" not in content

if __name__ == '__main__':
    pytest.main(["-v", "tests/test_optimize_sort_rows.py"])
