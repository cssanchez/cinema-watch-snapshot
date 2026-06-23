from apply_ux_improvements import transform_12_add_aria_live_to_results

def test_transform_12_adds_aria_live():
    html_input = '''
        <div class="front-screening-groups" data-front-advanced-results></div>
        <div class="empty">No results</div>
    '''
    expected = '''
        <div class="front-screening-groups" data-front-advanced-results aria-live="polite" role="status"></div>
        <div class="empty" aria-live="polite" role="status">No results</div>
    '''
    assert transform_12_add_aria_live_to_results(html_input) == expected
