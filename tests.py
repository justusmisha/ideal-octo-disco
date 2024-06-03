import math

from utils.data_calculator.roof_calculator import RoofCalculator
from utils.data_calculator.srub_calculator import SrubCalculator

c = SrubCalculator(a=3, b=6, h=2.20, d=20, extra_wall=False)
print(c.srub_price())
