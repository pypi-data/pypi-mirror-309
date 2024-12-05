def calculate_electricity_bill(total_usage_kwh, days):
    # Define the rate blocks
    block1_limit = 200
    block1_rate = 0.218

    block2_limit = 100
    block2_rate = 0.334

    block3_limit = 300
    block3_rate = 0.516

    block4_limit = 300
    block4_rate = 0.546

    block5_limit = 500
    block5_rate = 0.571  # Above 900 kWh

    sst_rate = 0.06  # 6% sst
    kwtbb_rate = 0.016  # 1.6% kwttb

    # Calculate base bill amount
    bill_amount = 0.0
    usage_kwh = total_usage_kwh

    if usage_kwh <= block1_limit:
        bill_amount = usage_kwh * block1_rate
    else:
        bill_amount += block1_limit * block1_rate
        usage_kwh -= block1_limit

        if usage_kwh <= block2_limit:
            bill_amount += usage_kwh * block2_rate
        else:
            bill_amount += block2_limit * block2_rate
            usage_kwh -= block2_limit

            if usage_kwh <= block3_limit:
                bill_amount += usage_kwh * block3_rate
            else:
                bill_amount += block3_limit * block3_rate
                usage_kwh -= block3_limit

                if usage_kwh <= block4_limit:
                    bill_amount += usage_kwh * block4_rate
                else:
                    bill_amount += block4_limit * block4_rate
                    usage_kwh -= block4_limit

                    if usage_kwh <= block5_limit:
                        bill_amount += usage_kwh * block5_rate

    # Kira KWTBB (1.6% daripada jumlah bil)
    kwtbb = round(bill_amount * kwtbb_rate if total_usage_kwh > 300 else 0, ndigits=1)

    # Kira SST (6% bagi bil yang melebihi 600 kWh)
    if days >= 28:
        sst = (bill_amount - (block1_limit * block1_rate + block2_limit * block2_rate + block3_limit * block3_rate)) * sst_rate if total_usage_kwh > 600 else 0
    else:
        sst = bill_amount * sst_rate

    # Jumlah bil akhir
    total_bill = bill_amount + kwtbb + sst

    return  bill_amount, sst, kwtbb, total_bill
