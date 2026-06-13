import pytest
from optimize_dom_array_from import process_file
from pathlib import Path
import tempfile

def test_map_keys_reduce_replacement():
    original_html = """        if (venueBuckets.size) {
          const bucketKey = Array.from(venueBuckets.keys()).reduce((best, current) => {
            const bestCount = venueBuckets.get(best) || 0;
            const currentCount = venueBuckets.get(current) || 0;
            if (currentCount !== bestCount) {
              return currentCount > bestCount ? current : best;
            }
            return current.localeCompare(best) < 0 ? current : best;
          });
          const [provider, venueKey, venueName, venueHref] = bucketKey.split('||');"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as temp_file:
        temp_file.write(original_html)
        temp_path = temp_file.name

    try:
        assert process_file(temp_path) == True

        with open(temp_path, 'r') as f:
            content = f.read()

        assert "Array.from(venueBuckets.keys()).reduce" not in content
        assert "for (const [currentKey, currentCount] of venueBuckets.entries()) {" in content
        assert "let bucketKey = null;" in content
        assert "let bestCount = -1;" in content
    finally:
        Path(temp_path).unlink()

if __name__ == '__main__':
    pytest.main(['-v', __file__])
