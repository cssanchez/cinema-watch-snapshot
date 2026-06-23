import pytest
from optimize_sort_rows import RE_SORT

def test_re_sort_matches_original_content():
    content = """
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
    match = RE_SORT.search(content)
    assert match is not None

def test_re_sort_does_not_match_optimized_content():
    content = """
      // ⚡ Bolt Optimization: Memoize identity string concatenation in sort comparators to prevent excessive O(N log N) memory allocations and reduce GC pressure.
      const _sortTitleKeyCache = new WeakMap();
      const _sortTimeKeyCache = new WeakMap();
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
            let leftKey = _sortTitleKeyCache.get(left);
            if (leftKey === undefined) {
              leftKey = `${left.date_iso}|${left.time_label}|${left.movie_title}`;
              _sortTitleKeyCache.set(left, leftKey);
            }
            let rightKey = _sortTitleKeyCache.get(right);
            if (rightKey === undefined) {
              rightKey = `${right.date_iso}|${right.time_label}|${right.movie_title}`;
              _sortTitleKeyCache.set(right, rightKey);
            }
            return leftKey.localeCompare(rightKey);
          });
          return nextRows;
        }
        nextRows.sort((left, right) => {
          let leftKey = _sortTimeKeyCache.get(left);
          if (leftKey === undefined) {
            leftKey = `${left.date_iso}|${left.time_label}`;
            _sortTimeKeyCache.set(left, leftKey);
          }
          let rightKey = _sortTimeKeyCache.get(right);
          if (rightKey === undefined) {
            rightKey = `${right.date_iso}|${right.time_label}`;
            _sortTimeKeyCache.set(right, rightKey);
          }
          return leftKey.localeCompare(rightKey);
        });
        return nextRows;
      }
"""
    match = RE_SORT.search(content)
    assert match is None
