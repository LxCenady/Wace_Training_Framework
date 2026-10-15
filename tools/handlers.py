"""Built-in subject capabilities. Data packs name handlers; they never provide executable code."""
from markpoints import points, rubric
from functools import partial

KEY_PARSERS = {'ticks': points, 'description-marks': rubric}  # maths tick keys; science Description/Marks keys
CHECKERS = {'sympy', 'none'}


def validate(profile):
    for field, available in (('key_style', KEY_PARSERS), ('checker', CHECKERS)):
        if not isinstance(profile.get(field), str) or profile[field] not in available:
            raise ValueError(f'Unsupported {field}: {profile.get(field)}')
    tolerance = profile.get('checker_tolerance', 5e-3)  # relative; 0 = only correctly rounded answers (money)
    if type(tolerance) not in (int, float) or not 0 <= tolerance <= 0.05:
        raise ValueError('checker_tolerance must be a number from 0 to 0.05')
    if not isinstance(profile.get('key_band_continuation', False), bool):
        raise ValueError('key_band_continuation must be boolean')
    if profile.get('key_band_continuation') and profile.get('key_style') != 'description-marks':
        raise ValueError('key_band_continuation requires description-marks')


def key_parser(profile):
    validate(profile)
    if profile.get('key_band_continuation'):
        return partial(rubric, band_continuation=True)
    return KEY_PARSERS[profile['key_style']]
