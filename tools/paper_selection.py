"""Optional section question counts: retain the pool, count only the required answers."""
import math


def validate(section):
    count = section.get('answer_count')
    if count is not None and (type(count) is not int or count < 1):
        raise ValueError('answer_count must be a positive integer')


def total(section, marks):
    """Maximum attainable section marks, independent of any student's earned marks."""
    validate(section)
    marks = list(marks)
    if any(type(m) not in (int, float) or not math.isfinite(m) or m <= 0 for m in marks):
        raise ValueError('Question marks must be positive')
    count = section.get('answer_count', len(marks))
    if count > len(marks):
        raise ValueError('Not enough questions for answer_count')
    return sum(sorted(marks, reverse=True)[:count])


def select(section, questions, chosen=None):
    """Questions are (ID, marks). Choice sections require explicit IDs, never best earned scores."""
    validate(section)
    questions = list(questions)
    by_id = dict(questions)
    if len(by_id) != len(questions):
        raise ValueError('Duplicate question IDs')
    if 'answer_count' not in section:
        if chosen is not None:
            raise ValueError('This section requires every question')
        return questions
    if chosen is None:
        raise ValueError('Explicit question selection required')
    chosen = list(chosen)
    if (len(chosen) != section['answer_count'] or len(set(chosen)) != len(chosen)
            or set(chosen) - set(by_id)):
        raise ValueError('Invalid question selection')
    return [(qid, marks) for qid, marks in questions if qid in chosen]
