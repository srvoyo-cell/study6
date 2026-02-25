```python
import sympy as sp

# Define the variable
x = sp.symbols('x')

# Define the function
f = x**2

# Compute the integral
integral = sp.integrate(f, (x, 0, 1))

# Print the result
print(integral)
```
