"""
create universe data
"""
import pandas as pd
import qis as qis
from typing import List
from enum import Enum
from bbg_fetch import fetch_fundamentals, fetch_field_timeseries_per_tickers

START_DATE = pd.Timestamp('31Dec2014')  # pd.Timestamp('03Aug2001')
END_DATE = pd.Timestamp.now().normalize()

FILE_NAME = 'PBA EQ'

from quant_screener import Universe, FILE_NAME


def get_universe_tickers(local_path: str,
                         universe: Universe = Universe.SAMPLE,
                         file_name: str = FILE_NAME
                         ) -> List[str]:
    """
    read tickers from  file_name by universe
    """
    df = qis.load_df_from_excel(file_name=file_name, local_path=local_path, sheet_name=universe.value)
    tickers = df['Ticker'].to_list()
    tickers_split = [x.split(' ') for x in tickers]
    tickers = [f"{x[0].upper()} {x[1].upper()} {x[-1]}" for x in tickers_split]
    tickers = list(set(tickers))

    if universe == Universe.GLOBAL:  # add etf tickers
        df = qis.load_df_from_excel(file_name=file_name, local_path=local_path, sheet_name='etfs')
        for ticker, country in zip(df['Primary Ticker**'].astype(str), df['Country'].astype(str)):
            if not ticker == 'nan' and not country == 'nan':
                tickers.append(f"{ticker} {country} Equity")
    return tickers


def create_universe_data(local_path: str = None,
                         file_name: str = FILE_NAME,
                         universes: List[Universe] = (Universe.SAMPLE, Universe.GLOBAL, ),
                         benchmark_tickers: List[str] = ('NDDUWI Index', 'LGTRTRUU Index',)
                         ) -> None:
    """
    read tickers from  file_name with sheets
    """
    price_dfs = {}
    for universe in universes:
        tickers = get_universe_tickers(local_path=local_path, universe=universe, file_name=file_name)
        price_timeseries = fetch_field_timeseries_per_tickers(tickers=tickers, field='px_last',
                                                              start_date=START_DATE, end_date=END_DATE)
        fundamentals = fetch_fundamentals(tickers=tickers, fields=['security_name', 'industry_sector', 'id_isin',
                                                                   'crncy', '3mo_put_imp_vol'])
        price_dfs[f"{universe.value}_price"] = price_timeseries
        price_dfs[f"{universe.value}_fundamentals"] = fundamentals

    benchmark_prices = fetch_field_timeseries_per_tickers(tickers=benchmark_tickers,
                                                          field='px_last',
                                                          start_date=START_DATE, end_date=END_DATE)
    price_dfs['benchmark_prices'] = benchmark_prices
    qis.save_df_to_excel(data=price_dfs, mode='a', file_name=FILE_NAME, local_path=local_path)


class UnitTests(Enum):
    GET_UNIVERSE_TICKERS = 1
    CREATE_UNIVERSE_DATA = 2


def run_unit_test(unit_test: UnitTests):

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    local_path = f"C://Users//artur//OneDrive//analytics//qdev//resources//basket_screener//"
    # local_path = f"C://Users//uarts//Python//quant_strats//resources//basket_screener//"

    if unit_test == UnitTests.GET_UNIVERSE_TICKERS:
        sample = get_universe_tickers(local_path=local_path, universe=Universe.SAMPLE)
        all = get_universe_tickers(local_path=local_path, universe=Universe.GLOBAL)
        print(qis.assert_list_subset(all, sample))

    elif unit_test == UnitTests.CREATE_UNIVERSE_DATA:
        create_universe_data(local_path=local_path, universes=[Universe.NOV19])


if __name__ == '__main__':

    unit_test = UnitTests.CREATE_UNIVERSE_DATA

    is_run_all_tests = False
    if is_run_all_tests:
        for unit_test in UnitTests:
            run_unit_test(unit_test=unit_test)
    else:
        run_unit_test(unit_test=unit_test)
