"""Built-in subject capabilities. Data packs name handlers; they never provide executable code."""
from markpoints import points, rubric

KEY_PARSERS = {'ticks': points, 'description-marks': rubric}  # maths tick keys; science Description/Marks keys
CHECKERS = {'sympy', 'none'}


def validate(profile):
    for field, available in (('key_style', KEY_PARSERS), ('checker', CHECKERS)):
        if not isinstance(profile.get(field), str) or profile[field] not in available:
            raise ValueError(f'Unsupported {field}: {profile.get(field)}')


def key_parser(profile):
    validate(profile)
    return KEY_PARSERS[profile['key_style']]
