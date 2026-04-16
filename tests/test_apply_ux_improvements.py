import pytest
from apply_ux_improvements import (
    extract_sold_percentage,
    transform_1_demote_freshness,
    transform_2_add_time_context,
    transform_3_truncation_signal,
    transform_4_occupancy_highlight,
    transform_5_count_format,
    transform_6_add_disabled_styles,
    transform_7_add_csp
)

def test_transform_5_basic():
    """Test basic transformation with a single section and correct count."""
    content = """
    <section class="front-date-group">
        <div class="front-date-head">
            <strong>2026-04-08</strong>
            <span class="chip" data-i18n-count="shown" data-i18n-count-value="3">3 shown</span>
        </div>
        <div class="front-screening-list">
            <div class="front-screening-row">Row 1</div>
            <div class="front-screening-row">Row 2</div>
            <div class="front-screening-row">Row 3</div>
        </div>
    </section>
    """
    expected = """
    <section class="front-date-group">
        <div class="front-date-head">
            <strong>2026-04-08</strong>
            <span class="chip" data-i18n-count="shown" data-i18n-count-value="3">3 of 3 shown</span>
        </div>
        <div class="front-screening-list">
            <div class="front-screening-row">Row 1</div>
            <div class="front-screening-row">Row 2</div>
            <div class="front-screening-row">Row 3</div>
        </div>
    </section>
    """
    assert transform_5_count_format(content) == expected

def test_transform_5_multiple_sections():
    """Test that each section gets its own correct count."""
    content = """
    <section class="front-date-group">
        <span class="chip">2 shown</span>
        <div class="front-screening-row">A1</div>
        <div class="front-screening-row">A2</div>
    </section>
    <section class="front-date-group">
        <span class="chip">1 shown</span>
        <div class="front-screening-row">B1</div>
    </section>
    """
    result = transform_5_count_format(content)
    assert "2 of 2 shown" in result
    assert "1 of 1 shown" in result
    assert "2 of 1 shown" not in result

def test_transform_5_zero_rows():
    """Test scenario with zero screening rows."""
    content = """
    <section class="front-date-group">
        <span class="chip">0 shown</span>
    </section>
    """
    expected = """
    <section class="front-date-group">
        <span class="chip">0 of 0 shown</span>
    </section>
    """
    assert transform_5_count_format(content) == expected

def test_transform_5_outside_section():
    """Test that "shown" text outside of target sections is not transformed."""
    content = """
    <div class="other">5 shown</div>
    <section class="front-date-group">
        <span class="chip">1 shown</span>
        <div class="front-screening-row">Row 1</div>
    </section>
    """
    result = transform_5_count_format(content)
    assert '<div class="other">5 shown</div>' in result
    assert "1 of 1 shown" in result

def test_transform_5_multiple_labels_in_section():
    """Test multiple "shown" labels within a single section."""
    content = """
    <section class="front-date-group">
        <span class="chip">2 shown</span>
        <div class="front-screening-row">Row 1</div>
        <div class="front-screening-row">Row 2</div>
        <p>Actually >2 shown< here too</p>
    </section>
    """
    result = transform_5_count_format(content)
    assert "2 of 2 shown" in result
    assert "Actually >2 of 2 shown< here too" in result


def test_extract_sold_percentage():
    """Test extract_sold_percentage with various edge cases."""
    assert extract_sold_percentage("45% sold") == 45.0
    assert extract_sold_percentage("100% sold") == 100.0
    assert extract_sold_percentage("0% sold") == 0.0
    assert extract_sold_percentage("none sold") == 0.0
    assert extract_sold_percentage("50%sold") == 50.0 # handles missing space
    assert extract_sold_percentage("") == 0.0
    assert extract_sold_percentage("Sold out") == 0.0
    assert extract_sold_percentage("Only 5% sold so far") == 5.0
    assert extract_sold_percentage("123% sold") == 123.0
    assert extract_sold_percentage("45 % sold") == 0.0 # current regex doesn't handle space before %

def test_transform_1_demote_freshness():
    content = """
    .front-freshness {
      background: rgba(255, 255, 255, 0.035);
      padding: 0.9rem 1rem;
      border-radius: var(--radius-md);
    }
    .front-freshness strong {
      font-family: var(--heading-font);
      font-size: 1.1rem;
      font-weight: 600;
    }
    """
    result = transform_1_demote_freshness(content)
    assert "background: rgba(255, 255, 255, 0.02)" in result
    assert "padding: 0.6rem 0.8rem" in result
    assert "font-family: var(--ui-font)" in result
    assert "font-size: 0.9rem" in result
    # Check that original values are gone
    assert "rgba(255, 255, 255, 0.035)" not in result
    assert "padding: 0.9rem 1rem" not in result
    assert "var(--heading-font)" not in result
    assert "1.1rem" not in result

def test_transform_2_add_time_context():
    content = """
    <section class="front-date-group">
        <div class="front-date-head">...</div>
    </section>
    <section class="front-date-group">
        <div class="front-date-head">...</div>
    </section>
    """
    result = transform_2_add_time_context(content)
    assert result.count('<div class="screening-time-context"') == 2
    assert "Coming up</span></div>\n    <section class=\"front-date-group\">" in result

def test_transform_3_truncation_signal():
    content = """
    <style>
      .some-class { color: red; }
    </style>
    <a class="text-link" href="/link" data-i18n-source>See all</a>
    """
    result = transform_3_truncation_signal(content)
    assert ".button-see-all {" in result
    assert '<a class="button-see-all" href="/link" data-i18n-source>See all</a>' in result
    assert '<a class="text-link"' not in result

def test_transform_4_occupancy_highlight():
    content = """
    <style>
      .some-class { color: red; }
    </style>
    <div class="front-screening-row">
        <div class="front-screening-copy">45% sold</div>
    </div>
    <div class="front-screening-row">
        <div class="front-screening-copy">50% sold</div>
    </div>
    <div class="front-screening-row">
        <div class="front-screening-copy">99% sold</div>
    </div>
    """
    result = transform_4_occupancy_highlight(content)
    assert ".screening-high-occupancy {" in result
    # Only 50% and 99% should have the class
    assert result.count("screening-high-occupancy") == 3 # 1 for CSS class definition, 2 for the matching elements
    assert '<div class="front-screening-row screening-high-occupancy">\n        <div class="front-screening-copy">50% sold</div>' in result
    assert '<div class="front-screening-row screening-high-occupancy">\n        <div class="front-screening-copy">99% sold</div>' in result
    assert '<div class="front-screening-row">\n        <div class="front-screening-copy">45% sold</div>' in result

def test_transform_6_add_disabled_styles():
    """Test that disabled styles are injected correctly."""
    content = "<style>\n  </style>"
    result = transform_6_add_disabled_styles(content)
    assert "button:disabled" in result
    assert "opacity: 0.5;" in result
    assert "cursor: not-allowed;" in result

def test_transform_6_add_disabled_styles_no_duplicate():
    """Test that disabled styles are not injected if already present."""
    content = "<style>\n    button:disabled { opacity: 0.5; }\n  </style>"
    result = transform_6_add_disabled_styles(content)
    # Should only appear once (the one we passed in)
    assert result.count("button:disabled") == 1


def test_transform_7_add_csp():
    content_with_charset = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Test</title>
</head>
<body></body>
</html>"""

    result = transform_7_add_csp(content_with_charset)
    assert '<meta http-equiv="Content-Security-Policy"' in result
    assert '<meta charset="utf-8">\n  <meta http-equiv="Content-Security-Policy"' in result

    content_with_head = """<!DOCTYPE html>
<html>
<head>
<title>Test</title>
</head>
<body></body>
</html>"""

    result2 = transform_7_add_csp(content_with_head)
    assert '<meta http-equiv="Content-Security-Policy"' in result2
    assert '<head>\n  <meta http-equiv="Content-Security-Policy"' in result2

    # Check idempotent behavior
    result3 = transform_7_add_csp(result)
    assert result3.count('<meta http-equiv="Content-Security-Policy"') == 1
def test_transform_2_basic():
    """Test basic transformation to add time context."""
    content = """
    <section class="front-date-group">
        <div>Some content</div>
    </section>
    """
    expected = """
    <div class="screening-time-context" style="display:flex; align-items:center; gap:0.5rem; padding:1rem; color:var(--accent); font-size:0.95rem;"><span style="color:var(--muted);">Coming up</span></div>
    <section class="front-date-group">
        <div>Some content</div>
    </section>
    """
    assert transform_2_add_time_context(content) == expected

def test_transform_2_multiple():
    """Test adding time context to multiple sections."""
    content = """
    <section class="front-date-group">
        <div>Section 1</div>
    </section>
    <section class="front-date-group">
        <div>Section 2</div>
    </section>
    """
    expected = """
    <div class="screening-time-context" style="display:flex; align-items:center; gap:0.5rem; padding:1rem; color:var(--accent); font-size:0.95rem;"><span style="color:var(--muted);">Coming up</span></div>
    <section class="front-date-group">
        <div>Section 1</div>
    </section>
    <div class="screening-time-context" style="display:flex; align-items:center; gap:0.5rem; padding:1rem; color:var(--accent); font-size:0.95rem;"><span style="color:var(--muted);">Coming up</span></div>
    <section class="front-date-group">
        <div>Section 2</div>
    </section>
    """
    assert transform_2_add_time_context(content) == expected

def test_transform_2_no_match():
    """Test when there is no matching section or spacing."""
    content = """<section class="front-date-group">
        <div>No leading newline + 4 spaces</div>
    </section>
    <section class="other-group">
        <div>Not a date group</div>
    </section>"""
    assert transform_2_add_time_context(content) == content

def test_transform_4_css_injection():
    """Test that CSS is injected correctly if not present."""
    content = "<style></style>"
    result = transform_4_occupancy_highlight(content)
    assert ".screening-high-occupancy" in result
    assert "background: rgba(240, 139, 101, 0.15);" in result

def test_transform_4_css_no_duplicate():
    """Test that CSS is not injected if already present."""
    content = "<style>.screening-high-occupancy {}</style>"
    result = transform_4_occupancy_highlight(content)
    # Should only appear once (the one we passed in)
    assert result.count(".screening-high-occupancy") == 1

def test_transform_4_high_occupancy():
    """Test that high occupancy class is added for >= 50% sold."""
    content = """
    <div class="front-screening-row">
        <span>50% sold</span>
        <div class="front-screening-copy">Some text</div>
    </div>
    """
    result = transform_4_occupancy_highlight(content)
    assert '<div class="front-screening-row screening-high-occupancy">' in result

def test_transform_4_low_occupancy():
    """Test that high occupancy class is NOT added for < 50% sold."""
    content = """
    <div class="front-screening-row">
        <span>49% sold</span>
        <div class="front-screening-copy">Some text</div>
    </div>
    """
    result = transform_4_occupancy_highlight(content)
    assert '<div class="front-screening-row screening-high-occupancy">' not in result
    assert '<div class="front-screening-row">' in result

def test_transform_4_no_occupancy():
    """Test that high occupancy class is NOT added when no sold percentage is present."""
    content = """
    <div class="front-screening-row">
        <span>Available</span>
        <div class="front-screening-copy">Some text</div>
    </div>
    """
    result = transform_4_occupancy_highlight(content)
    assert '<div class="front-screening-row screening-high-occupancy">' not in result
    assert '<div class="front-screening-row">' in result
def test_transform_1_demote_freshness_full():
    """Test full transformation of .front-freshness and .front-freshness strong."""
    content = """
    <style>
    .front-freshness strong {
      font-family: var(--heading-font);
      font-weight: 600;
      font-size: 1.1rem;
    }
    .front-freshness {
      padding: 0.9rem 1rem;
      background: rgba(255, 255, 255, 0.035);
      border-radius: var(--radius-md);
    }
    </style>
    """
    expected = """
    <style>
    .front-freshness strong {
      font-family: var(--ui-font);
      font-weight: 600;
      font-size: 0.9rem;
    }
    .front-freshness {
      padding: 0.6rem 0.8rem;
      background: rgba(255, 255, 255, 0.02);
      border-radius: var(--radius-md);
    }
    </style>
    """
    assert transform_1_demote_freshness(content) == expected

def test_transform_1_demote_freshness_no_match():
    """Test that content without matching CSS rules remains unchanged."""
    content = """
    <style>
    .front-freshness strong {
      font-family: var(--ui-font);
      font-weight: 600;
      font-size: 0.9rem;
    }
    .other-class {
      padding: 0.9rem 1rem;
      background: rgba(255, 255, 255, 0.035);
    }
    </style>
    """
    assert transform_1_demote_freshness(content) == content

def test_transform_1_demote_freshness_partial():
    """Test partial match scenarios."""
    content = """
    <style>
    .front-freshness {
      padding: 0.9rem 1rem;
      border-radius: var(--radius-md);
    }
    </style>
    """
    expected = """
    <style>
    .front-freshness {
      padding: 0.6rem 0.8rem;
      border-radius: var(--radius-md);
    }
    </style>
    """
    assert transform_1_demote_freshness(content) == expected

from apply_ux_improvements import transform_9_add_clear_filters_button

def test_transform_9_add_clear_filters_button():
    content = """
    <div class="form-actions front-advanced-actions">
              <button type="submit" class="button-pill" data-tone="accent" data-i18n-source>Filter</button>
    </div>
    """
    expected = """
    <div class="form-actions front-advanced-actions">
              <button type="submit" class="button-pill" data-tone="accent" data-i18n-source>Filter</button>
              <button type="button" class="button-pill" data-tone="neutral" data-front-advanced-reset="true" data-i18n-source>Clear filters</button>
    </div>
    """
    result = transform_9_add_clear_filters_button(content)
    assert result == expected

def test_transform_9_add_clear_filters_button_no_duplicate():
    content = """
    <div class="form-actions front-advanced-actions">
              <button type="submit" class="button-pill" data-tone="accent" data-i18n-source>Filter</button>
              <button type="button" class="button-pill" data-tone="neutral" data-front-advanced-reset="true" data-i18n-source>Clear filters</button>
    </div>
    """
    result = transform_9_add_clear_filters_button(content)
    assert result == content
