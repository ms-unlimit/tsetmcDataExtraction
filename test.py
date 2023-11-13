import finpy_tse as fpy


p = fpy.Get_IntradayTrades_History(
    stock='وخارزم',
    start_date='1400-11-15',
    end_date='1400-12-29',
    jalali_date=True,
    combined_datatime=False,
    show_progress=True)


print(p)
