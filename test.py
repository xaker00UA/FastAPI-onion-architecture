from decimal import Decimal

a = 3
b = 0.33

print(b)
print(a * b)
c, d = Decimal(str(b)), Decimal(a)
print(c * d)
