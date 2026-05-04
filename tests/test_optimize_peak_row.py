import pytest
from optimize_peak_row import process_file

def test_process_file_idempotency(tmp_path):
    test_file = tmp_path / "test.html"
    original_content = """        let peakRow = null;
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
    test_file.write_text(original_content, encoding="utf-8")

    assert process_file(test_file) is True
    patched_content = test_file.read_text(encoding="utf-8")
    assert "⚡ Bolt Optimization: Replaced O(N log N) sorting with O(N) reduction to find the peak row" in patched_content
    assert "reduce" in patched_content
    assert "sort(" not in patched_content

    assert process_file(test_file) is False
    assert test_file.read_text(encoding="utf-8") == patched_content
