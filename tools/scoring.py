"""Validate score metadata and aggregate section marks without inventing missing results."""
import math
import paper_selection


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate(profile):
    scoring = profile.get('scoring', {'mode': 'raw'})
    if not isinstance(scoring, dict) or scoring.get('mode') not in ('raw', 'section-weighted'):
        raise ValueError('Invalid scoring mode')
    sections = profile['sections']
    for section in sections:
        paper_selection.validate(section)
    if scoring['mode'] == 'section-weighted':
        shares = [s.get('share') for s in sections]
        if any(not number(w) or not 0 < w <= 1 for w in shares) or not math.isclose(sum(shares), 1, abs_tol=1e-9):
            raise ValueError('Section shares must be positive and sum to 1')
    for key in ('valid_from', 'valid_to'):
        if key in scoring and type(scoring[key]) is not int:
            raise ValueError('Invalid scoring year')
    if scoring.get('valid_to', 9999) < scoring.get('valid_from', 0):
        raise ValueError('Invalid scoring year range')


def score(profile, results, year=None, answered=None):
    """results = {code: (earned, possible)}. Partial coverage never yields a whole-paper percentage."""
    validate(profile)
    config = profile.get('scoring', {'mode': 'raw'})
    if year is not None and not config.get('valid_from', 0) <= year <= config.get('valid_to', 9999):
        raise ValueError('No verified scoring metadata for this year')
    sections = {s['code']: s for s in profile['sections']}
    if not results or set(results) - set(sections):
        raise ValueError('Unknown or empty score sections')
    for earned, possible in results.values():
        if not number(earned) or not number(possible) or possible <= 0 or not 0 <= earned <= possible:
            raise ValueError('Marks must satisfy 0 <= earned <= possible, possible > 0')
    earned = sum(pair[0] for pair in results.values())
    possible = sum(pair[1] for pair in results.values())
    complete = set(results) == set(sections)
    answered = {} if answered is None else answered
    if not isinstance(answered, dict) or set(answered) - set(sections):
        raise ValueError('Unknown answer selection sections')
    for code, section in sections.items():
        count = section.get('answer_count')
        if count is None or code not in results:
            continue
        ids = answered.get(code)
        if ids is None:
            complete = False  # practicing both alternatives never implies a valid whole-paper sitting
        elif (not isinstance(ids, list) or len(ids) != count or any(not isinstance(i, str) or not i for i in ids)
              or len(set(ids)) != len(ids)):
            raise ValueError('Invalid explicit answer selection')
    if config['mode'] == 'section-weighted':
        coverage = sum(sections[code]['share'] for code in results)
        contribution = 100 * sum(sections[c]['share'] * e / p for c, (e, p) in results.items())
        practice = contribution / coverage
    else:
        coverage = 1 if complete else None
        practice = 100 * earned / possible
        contribution = practice if complete else None
    return dict(earned=earned, possible=possible, complete=complete, coverage=coverage,
                practice_percent=practice, paper_percent=contribution if complete else None,
                weighted_contribution=contribution)
