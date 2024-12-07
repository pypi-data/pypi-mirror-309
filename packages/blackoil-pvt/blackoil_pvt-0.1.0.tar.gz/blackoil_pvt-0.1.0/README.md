# BlackOil PVT Library

`blackoil_pvt` is a Python library for calculating black oil PVT properties using the Standing method. It includes functions for:

- Bubble Point Pressure (\( P_b \))
- Solution Gas-Oil Ratio (\( R_s \))
- Oil Formation Volume Factor (\( B_o \))
- Oil Viscosity (\( \mu_o \))
- Gas Formation Volume Factor (\( B_g \))
- Gas Viscosity (\( \mu_g \))
- Oil Compressibility (\( C_o \))
- Gas Compressibility (\( C_g \))

## Installation
Clone the repository or install via pip once published.

## Usage
```python
from blackoil_pvt import calculate_bubble_point_pressure

# Example
Pb = calculate_bubble_point_pressure(Rs=600, SGg=0.85, T=200, API=35)
print(Pb)
