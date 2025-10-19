from sympy import symbols, integrate, sympify
from sympy.core.function import AppliedUndef
from sympy.integrals.integrals import Integral
import mpmath as mp
from scipy import integrate as sp_integrate
import numpy as np

def hybrid_integrate(expr, var='x', bounds=None, numeric_backend='scipy'):
    """
    Hybrid integration helper:
    - Tries SymPy for exact result
    - Falls back to numerical integration if needed
    
    Parameters
    ----------
    expr : str or sympy expression
        The integrand
    var : str
        Variable of integration
    bounds : tuple or None
        If None → indefinite integral
        If (a, b) → definite integral from a to b
    numeric_backend : 'scipy' or 'mpmath'
        Which numerical engine to use for fallback
    """
    x = symbols(var)
    expr = sympify(expr)

    try:
        if bounds is None:
            # Indefinite integral
            result = integrate(expr, x)
        else:
            a, b = bounds
            result = integrate(expr, (x, a, b))
        
        # If SymPy leaves it unevaluated, fallback
        if isinstance(result, (Integral, AppliedUndef)):
            raise ValueError("SymPy could not evaluate exactly.")
        
        return result
    except Exception:
        # Fallback to numerical
        f = lambda t: float(expr.subs(x, t))
        if bounds is None:
            raise ValueError("Numerical indefinite integrals not supported.")
        a, b = bounds
        if numeric_backend == 'scipy':
            val, err = sp_integrate.quad(f, a, b)
            return val
        elif numeric_backend == 'mpmath':
            return mp.quad(lambda t: expr.subs(x, t), [a, b])
        else:
            raise ValueError("Unknown backend.")

# -------------------------
# Examples
# -------------------------
print(hybrid_integrate("sin(x)", "x"))             # → -cos(x)
print(hybrid_integrate("exp(-x**2)", "x", (0, mp.inf)))  # → √π/2 numerically
