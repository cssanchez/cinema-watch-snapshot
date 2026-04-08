from apply_ux_improvements import (extract_sold_percentage, transform_2_add_time_context, transform_5_count_format)

import pytest
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
