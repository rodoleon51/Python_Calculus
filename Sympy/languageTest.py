import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

sp.init_printing()
x = sp.Symbol('x')
y = sp.Function('y')(x)

# First-order ODE: dy/dx = -2*y
ode1 = sp.Eq(y.diff(x), -2*y)
sol1 = sp.dsolve(ode1)
print("Solution:", sol1)

# With initial condition: y(0) = 1
sol1_ic = sp.dsolve(ode1, ics={y.subs(x, 0): 1})
print("Particular solution:", sol1_ic)

# Plotting
f = sp.lambdify(x, sol1_ic.rhs, 'numpy')
x_vals = np.linspace(0, 10, 100)
y_vals = f(x_vals)

plt.plot(x_vals, y_vals, label='y(x) = exp(-2x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title("Solution to y' = -2y with y(0)=1")
plt.grid(True)
plt.legend()
plt.show()