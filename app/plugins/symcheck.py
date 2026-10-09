"""Symbolic check. One job: compute each part's answer with SymPy, independently of any model's arithmetic,
and compare it with the answers the models claim.

The solver writes one SymPy expression per numeric part ("sympy"); the setter states its answer as a SymPy
value ("value"). Expressions are model-written code, so they are (1) parsed and checked against a whitelist
of node types and names — numbers, arithmetic, calls to known maths functions, unknown names become symbols;
no attributes, imports, dunders, lambdas or comprehensions — and (2) evaluated in a separate process with a
time limit. Parts that cannot be evaluated are reported as unchecked, never as wrong.
"""
import ast, json, os, random, subprocess, sys

ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call, ast.Name, ast.Load, ast.Constant, ast.List,
                 ast.Tuple, ast.keyword, ast.Compare, ast.Subscript, ast.Slice,
                 ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv,
                 ast.Eq, ast.Lt, ast.Gt, ast.LtE, ast.GtE, ast.NotEq)
FUNCS = ("sqrt exp log ln sin cos tan sec csc cot asin acos atan atan2 sinh cosh tanh pi E I oo diff integrate "
         "solve nsolve solveset limit simplify expand factor cancel apart trigsimp nsimplify Rational Abs Eq N "
         "Matrix binomial factorial Sum Min Max floor ceiling root cbrt re im arg conjugate Function dsolve "
         "Derivative Integral Symbol symbols Interval Piecewise S Normal Binomial Uniform Bernoulli Exponential "
         "P expectation variance std cross dot norm").split()
COMPLEX = {"z", "w", "u", "v"}  # names that usually denote complex numbers in MAS


def safe(expr):
    """Parse and whitelist; returns the AST or raises ValueError."""
    tree = ast.parse(expr.replace("^", "**"), mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"not allowed: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id.startswith("_"):
            raise ValueError("underscore names are not allowed")
        if isinstance(node, ast.Call) and not isinstance(node.func, (ast.Name, ast.Call)):
            raise ValueError("only plain function calls are allowed")
    return tree


def namespace(tree):
    import sympy
    import sympy.stats as st
    ns = {n: getattr(sympy, n) for n in FUNCS if hasattr(sympy, n)}
    ns.update(ln=sympy.log, P=st.P, expectation=st.E, variance=st.variance, std=st.std, Normal=st.Normal,
              Binomial=st.Binomial, Uniform=st.Uniform, Bernoulli=st.Bernoulli, Exponential=st.Exponential,
              cross=lambda a, b: sympy.Matrix(a).cross(sympy.Matrix(b)),
              dot=lambda a, b: sympy.Matrix(a).dot(sympy.Matrix(b)), norm=lambda a: sympy.Matrix(a).norm())
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in ns:
            ns[node.id] = sympy.Symbol(node.id) if node.id in COMPLEX else sympy.Symbol(node.id, real=True)
    ns["__builtins__"] = {}
    return ns


def numbers(value, subs):
    """Flatten a SymPy result (number, expression, list/tuple/set/dict/FiniteSet, Eq) into complex numbers."""
    import sympy
    if isinstance(value, dict):
        value = list(value.values())
    if isinstance(value, sympy.Equality):
        value = value.rhs - value.lhs
    if isinstance(value, (list, tuple, set, sympy.FiniteSet)) or (hasattr(value, "is_Matrix") and value.is_Matrix):
        out = []
        for v in value:
            out += numbers(v, subs)
        return out
    v = sympy.sympify(value)
    if v.free_symbols:
        v = v.subs({s: subs.setdefault(s.name, sympy.Rational(random.Random(s.name).randint(130, 970), 100))
                    for s in v.free_symbols})
    return [complex(sympy.N(v, 15))]


def evaluate(pairs):
    """Worker-process entry: [(label, expr, [claims…])] -> {label: (status, detail)}."""
    out = {}
    for label, expr, claims in pairs:
        try:
            subs = {}
            tree = safe(expr)
            got = numbers(eval(compile(tree, "<sympy>", "eval"), namespace(tree)), subs)
            if not got:
                out[label] = ("skip", "expression gave no value")
                continue
            for who, claim in claims:
                ctree = safe(claim)
                want = numbers(eval(compile(ctree, "<claim>", "eval"), namespace(ctree)), subs)
                miss = [w for w in want if not any(close(w, g) for g in got)]
                if miss:
                    out[label] = ("mismatch", f"SymPy gives {fmt(got)} but the {who} says {fmt(want)}")
                    break
            else:
                out[label] = ("ok", fmt(got))
        except Exception as e:  # unparseable / unsupported / sympy error: unchecked, not wrong
            out[label] = ("skip", f"{type(e).__name__}: {str(e)[:120]}")
    return out


def close(a, b, rel=5e-3, absolute=1e-6):
    return abs(a - b) <= max(absolute, rel * max(abs(a), abs(b)))


def fmt(vals):
    return ", ".join(f"{v.real:.6g}" if abs(v.imag) < 1e-9 else f"{v.real:.4g}{v.imag:+.4g}i" for v in vals[:6])


def worker():
    """`WTF --symcheck` / `python main.py --symcheck`: JSON pairs on stdin -> JSON results on stdout."""
    pairs = json.load(sys.stdin)
    json.dump(evaluate([(l, e, [tuple(c) for c in cs]) for l, e, cs in pairs]), sys.stdout)


def check(pairs, timeout=40):
    """Evaluate in a child process of this same program; anything not finished in time is reported as unchecked."""
    if not pairs:
        return {}
    frozen = getattr(sys, "frozen", False)
    main = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    cmd = [sys.executable] + ([] if frozen else [main]) + ["--symcheck"]
    try:
        out = subprocess.run(cmd, input=json.dumps(pairs), capture_output=True, text=True, encoding="utf-8",
                             timeout=timeout, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        return {label: tuple(v) for label, v in json.loads(out.stdout).items()}
    except subprocess.TimeoutExpired:
        return {label: ("skip", f"timed out after {timeout}s") for label, _, _ in pairs}
    except (ValueError, OSError) as e:
        return {label: ("skip", f"checker unavailable: {type(e).__name__}") for label, _, _ in pairs}


def setup(k):
    k.provide("symcheck", check)
