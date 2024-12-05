# tnb_bill

A Python package to calculate TNB electricity bills based on usage, with support for KWTBB and SST.

## How to install in Google Colab
```
!pip install tnb_bill
```

## Example of usage
```
from tnb_bill import calculate_electricity_bill

total_usage_kwh = 1400
days = 30
bill_amount, sst, kwtbb, total_bill = calculate_electricity_bill(total_usage_kwh, days)

print(f"Bill Amount : RM {bill_amount:.2f}")
print(f"SST : {sst:.2f}")
print(f"KWTBB : {kwtbb:.2f}")
print(f"Total Electricity Bill (including 6% SST) for {total_usage_kwh} kWh is: RM {total_bill:.2f}")
```

