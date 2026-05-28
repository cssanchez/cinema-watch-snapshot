import pytest
from apply_ux_improvements import transform_12_dynamic_results_a11y

def test_transform_12_dynamic_results_a11y():
    # Test advanced results container
    content = '<div class="front-screening-groups" data-front-advanced-results></div>'
    expected = '<div class="front-screening-groups" data-front-advanced-results aria-live="polite" role="status"></div>'
    assert transform_12_dynamic_results_a11y(content) == expected

    # Test empty state messages
    content2 = '<div class="empty">No IMAX screenings</div>'
    expected2 = '<div class="empty" aria-live="polite" role="status">No IMAX screenings</div>'
    assert transform_12_dynamic_results_a11y(content2) == expected2

    # Test summary box
    content3 = '<div class="front-advanced-summary" data-front-advanced-signals hidden></div>'
    expected3 = '<div class="front-advanced-summary" data-front-advanced-signals aria-live="polite" role="status" hidden></div>'
    assert transform_12_dynamic_results_a11y(content3) == expected3

    # Test idempotency
    assert transform_12_dynamic_results_a11y(expected) == expected
    assert transform_12_dynamic_results_a11y(expected2) == expected2
    assert transform_12_dynamic_results_a11y(expected3) == expected3
