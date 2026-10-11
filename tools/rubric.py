"""Data-only scoring trees; concept coverage is diagnostic, never additive credit."""
import math


def _marks(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def validate(root, printed_marks=None):
    """Return indexed nodes and maxima. Reject ambiguous ownership or references."""
    nodes, maxima, visiting = {}, {}, set()

    def walk(node):
        if not isinstance(node, dict) or not isinstance(node.get('id'), str) or not node['id']:
            raise ValueError('Every rubric node needs an ID')
        ident = node['id']
        if ident in nodes or id(node) in visiting:
            raise ValueError('Duplicate or cyclic rubric node: ' + ident)
        visiting.add(id(node))
        nodes[ident] = node
        kind = node.get('kind')
        if kind == 'award':
            maximum = node.get('max_marks')
            if not _marks(maximum) or maximum == 0 or 'children' in node:
                raise ValueError('Invalid award: ' + ident)
            for field in ('knowledge', 'patterns'):
                tags = node.get(field, [])
                if not isinstance(tags, list) or any(not isinstance(t, str) or not t for t in tags) or len(tags) != len(set(tags)):
                    raise ValueError('Invalid award tags: ' + ident)
            band = node.get('positive_band')
            if band is not None and (not isinstance(band, list) or len(band) != 2 or
                                     not all(_marks(n) for n in band) or not 0 < band[0] <= band[1] == maximum):
                raise ValueError('Invalid positive band: ' + ident)
        elif kind in ('sum', 'best', 'select'):
            children = node.get('children')
            if not isinstance(children, list) or not children:
                raise ValueError('Empty scoring group: ' + ident)
            values = [walk(child) for child in children]
            if kind == 'best':
                maximum = max(values)
            elif kind == 'select':
                take = node.get('take')
                if type(take) is not int or not 1 <= take <= len(values):
                    raise ValueError('Invalid choice count: ' + ident)
                maximum = sum(sorted(values, reverse=True)[:take])
            else:
                maximum = sum(values)
        else:
            raise ValueError('Unknown rubric node kind: ' + str(kind))
        if 'cap' in node:
            cap = node['cap']
            if not _marks(cap) or cap > maximum:
                raise ValueError('Invalid cap: ' + ident)
            maximum = min(maximum, cap)
        maxima[ident] = maximum
        visiting.remove(id(node))
        return maximum

    maximum = walk(root)
    for ident, node in nodes.items():
        refs = node.get('requires', [])
        if (not isinstance(refs, list) or any(not isinstance(r, str) for r in refs) or
                len(refs) != len(set(refs)) or any(r not in nodes or r == ident for r in refs)):
            raise ValueError('Invalid dependency: ' + ident)
        conditions = node.get('conditions', [])
        if not isinstance(conditions, list) or any(not isinstance(c, str) or not c for c in conditions):
            raise ValueError('Invalid review condition: ' + ident)
        limits = node.get('conditional_caps', [])
        if not isinstance(limits, list):
            raise ValueError('Invalid conditional caps: ' + ident)
        for limit in limits:
            if (not isinstance(limit, dict) or not isinstance(limit.get('condition'), str) or
                    not limit['condition'] or not _marks(limit.get('cap')) or limit['cap'] > maxima[ident]):
                raise ValueError('Invalid conditional cap: ' + ident)
    active, done = set(), set()

    def dependencies(ident):
        if ident in active:
            raise ValueError('Cyclic scoring dependencies')
        if ident in done:
            return
        active.add(ident)
        node = nodes[ident]
        for other in node.get('requires', []) + [c['id'] for c in node.get('children', [])]:
            dependencies(other)
        active.remove(ident)
        done.add(ident)

    for ident in nodes:
        dependencies(ident)
    if printed_marks is not None and (not _marks(printed_marks) or not math.isclose(maximum, printed_marks, abs_tol=1e-9)):
        raise ValueError('Rubric maximum differs from printed marks')
    return nodes, maxima


def validate_associations(root, knowledge_ids, pattern_ids):
    """A formal tagged rubric needs explicit, catalogue-backed links on every award."""
    nodes, _ = validate(root)
    available = {'knowledge': set(knowledge_ids), 'patterns': set(pattern_ids)}
    for ident, node in nodes.items():
        if node['kind'] != 'award':
            continue
        for field, catalogue in available.items():
            tags = node.get(field, [])
            if not tags or set(tags) - catalogue:
                raise ValueError('Missing or unknown ' + field + ' association: ' + ident)


def score(root, credits, conditions=None):
    """Missing award credits mean zero; missing required judgments produce bounds.

    conditional_caps apply when their reviewed condition is true. `requires`
    requires positive credit on every referenced node. No pack expression executes.
    """
    nodes, maxima = validate(root)
    conditions = conditions or {}
    awards = {ident for ident, n in nodes.items() if n['kind'] == 'award'}
    if not isinstance(credits, dict) or set(credits) - awards:
        raise ValueError('Credit must reference award IDs only')
    if any(type(v) is not bool for v in conditions.values()):
        raise ValueError('Review conditions must be booleans')
    condition_ids = {c for n in nodes.values() for c in n.get('conditions', [])}
    condition_ids.update(c['condition'] for n in nodes.values() for c in n.get('conditional_caps', []))
    if set(conditions) - condition_ids:
        raise ValueError('Unknown review condition')
    for ident, credit in credits.items():
        if not _marks(credit) or credit > maxima[ident]:
            raise ValueError('Award credit out of range: ' + ident)
        band = nodes[ident].get('positive_band')
        if band and 0 < credit < band[0]:
            raise ValueError('Credit below positive band: ' + ident)
    cache, unresolved = {}, set()

    def evaluate(ident):
        if ident in cache:
            return cache[ident]
        node = nodes[ident]
        kind = node['kind']
        if kind == 'award':
            lower = upper = credits.get(ident, 0)
        else:
            pairs = [evaluate(c['id']) for c in node['children']]
            def aggregate(values):
                if kind == 'best':
                    return max(values)
                if kind == 'select':
                    return sum(sorted(values, reverse=True)[:node['take']])
                return sum(values)
            lower, upper = aggregate([p[0] for p in pairs]), aggregate([p[1] for p in pairs])
        lower, upper = min(lower, maxima[ident]), min(upper, maxima[ident])
        for required in node.get('requires', []):
            lo, hi = evaluate(required)
            if hi == 0:
                lower = upper = 0
            elif lo == 0:
                lower = 0
        for condition in node.get('conditions', []):
            if condition not in conditions and upper:
                unresolved.add(condition)
                lower = 0
            elif conditions.get(condition) is False:
                lower = upper = 0
        for limit in node.get('conditional_caps', []):
            condition, cap = limit['condition'], limit['cap']
            if condition not in conditions and upper > cap:
                unresolved.add(condition)
                lower = min(lower, cap)
            elif conditions.get(condition) is True:
                lower, upper = min(lower, cap), min(upper, cap)
        cache[ident] = (lower, upper)
        return cache[ident]

    lower, upper = evaluate(root['id'])
    resolved = math.isclose(lower, upper, abs_tol=1e-9)
    selections = {}
    for ident, node in nodes.items():
        if node['kind'] not in ('best', 'select'):
            continue
        choices = [(c['id'], evaluate(c['id'])) for c in node['children']]
        if any(not math.isclose(lo, hi, abs_tol=1e-9) for _, (lo, hi) in choices):
            selections[ident] = None
        else:
            # Stable source order breaks tied scores; no credit is counted twice.
            choices.sort(key=lambda c: c[1][0], reverse=True)
            take = 1 if node['kind'] == 'best' else node['take']
            selections[ident] = [c for c, (lo, _) in choices[:take] if lo > 0]
    return dict(earned=lower if resolved else None, lower=lower, upper=upper,
                possible=maxima[root['id']], resolved=resolved,
                unresolved_conditions=sorted(unresolved), credited_awards=dict(credits),
                selections=selections)


def coverage(root, field='knowledge'):
    """Maximum attainable tagged marks per atom/pattern, preserving route/cap rules.

    Each entry is a separate diagnostic projection, so entries must not be summed.
    A two-mark criterion linked to two atoms supplies two overlapping projections.
    """
    nodes, _ = validate(root)
    if field not in ('knowledge', 'patterns'):
        raise ValueError('Unknown association field')
    tags = sorted({t for n in nodes.values() if n['kind'] == 'award' for t in n.get(field, [])})
    result = {}
    for tag in tags:
        def project(node):
            kind = node['kind']
            if kind == 'award':
                value = node['max_marks'] if tag in node.get(field, []) else 0
            else:
                values = [project(child) for child in node['children']]
                if kind == 'best':
                    value = max(values)
                elif kind == 'select':
                    value = sum(sorted(values, reverse=True)[:node['take']])
                else:
                    value = sum(values)
            return min(value, node.get('cap', value))
        # Untagged prerequisites can be satisfied without contributing to this
        # projection. Pending conditions do not prove a smaller potential maximum.
        result[tag] = project(root)
    return result
