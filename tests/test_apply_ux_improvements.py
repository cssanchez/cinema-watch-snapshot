import pytest
from apply_ux_improvements import (
    extract_sold_percentage,
    transform_1_demote_freshness,
    transform_5_count_format,
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
