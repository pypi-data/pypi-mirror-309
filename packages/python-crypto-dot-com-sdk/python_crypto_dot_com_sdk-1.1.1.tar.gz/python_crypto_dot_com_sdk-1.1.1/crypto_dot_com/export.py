"""Export tools
"""

import datetime
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas

from crypto_dot_com.client import CryptoAPI
from crypto_dot_com.data_models.order_history import OrderHistoryDataMessage
from crypto_dot_com.enums import StatusEnum


def read_order_history_from_csv(
    filepath: str | Path,
    filter_by_status: list[StatusEnum] | list[str] | None = None,
    filter_by_instrument_name: str | None = None,
    return_type: str = "pydantic",
) -> list[OrderHistoryDataMessage] | pandas.DataFrame:
    df = pandas.read_csv(filepath)
    df = df.astype({"client_oid": "str", "order_id": "str"})
    if filter_by_status is not None:
        filter_by_status = [
            item for item in filter_by_status if (type(item) is str)
        ]
        filter_by_status += [
            item.value
            for item in filter_by_status
            if (isinstance(item, StatusEnum))
        ]
        df = df[df["status"].isin(filter_by_status)]
    if filter_by_instrument_name is not None:
        df = df[df["instrument_name"] == filter_by_instrument_name]

    # return based on return type
    if return_type.lower() == "pydantic":
        data: list[OrderHistoryDataMessage] = [
            OrderHistoryDataMessage(**row)  # type: ignore
            for row in df.to_dict(orient="records")
        ]
        return data
    elif return_type.lower() == "dataframe":
        return df
    else:
        raise ValueError(
            "return_type should be one of ['dataframe', 'pydantic']"
        )


def export_order_history(
    api_key: str,
    secret_key: str,
    filepath: str | Path,
    past_n_days: int = 0,
) -> int:
    """
    Downloads and saves order history data to the specified file path.

    If the file already exists at the given path, the function will read the
     existing data, append the new data, and remove any duplicate records based
     on the `order_id` column.

    The `past_n_days` parameter determines how many days' worth of data to
     download. By default, it is set to 0, meaning only today’s data will
     be downloaded and added to the file.

    Note that Crypto.com only allows up to 6 months of data to be downloaded,
    so running this function regularly is recommended.
    """
    if type(filepath) is str:
        filepath = Path(filepath)
    assert isinstance(filepath, Path)

    client = CryptoAPI(
        api_key=api_key,
        api_secret=secret_key,
        log_json_response_to_file=False,
    )

    # Download data from Crypto.com API
    all_data = []
    reference_date = datetime.date.today()
    for i in range(-1, past_n_days + 1):
        day = reference_date - datetime.timedelta(days=i)
        data = client.get_all_order_history_of_a_day(
            instrument_name=None, day=day
        )
        all_data.extend(data)

    # update all_data in case the file exist in the path
    if filepath.is_file():
        prev_data = read_order_history_from_csv(
            filepath=filepath, return_type="pydantic"
        )
        all_data.extend(prev_data)  # type: ignore

    df = pandas.DataFrame([item.model_dump() for item in all_data])
    df["exec_inst"] = df["exec_inst"].apply(json.dumps)
    df.drop_duplicates(subset="order_id", keep="first", inplace=True)
    df.to_csv(filepath)
    return len(df)


def export_user_balance(
    api_key: str,
    secret_key: str,
    filepath: str | Path,
    pie_chart_filepath: str | Path | None = None,
    figsize: tuple[float | int, float | int] = (8, 8),
    filter_values_in_pie_chart: float = 1.0,
) -> None:
    """Export user balance to give filepath

    filter_values_in_pie_chart used to only consider currencies with bigger
    than given market_value. By default it is 1 which means only the
    currencies or categories with market value of greater than 1 USD will
    be depicted in the graph.
    """
    if type(filepath) is str:
        filepath = Path(filepath)
    assert isinstance(filepath, Path)

    client = CryptoAPI(
        api_key=api_key,
        api_secret=secret_key,
        log_json_response_to_file=False,
    )

    df = client.get_user_balance_summary_as_df()
    if df is not None:
        df.to_csv(filepath, index=False)

    if pie_chart_filepath is None:
        return
    if type(pie_chart_filepath) is str:
        pie_chart_filepath = Path(filepath)
    assert isinstance(pie_chart_filepath, Path)

    portfolio = client.get_user_balance_summary()
    currencies = [
        item.currency for item in portfolio if item.market_value > 0.1
    ]
    market_values = [
        item.market_value for item in portfolio if item.market_value > 0.1
    ]

    plt.figure(figsize=figsize)
    plt.pie(
        market_values, labels=currencies, autopct="%1.1f%%", startangle=140
    )
    plt.title("Portfolio Allocation")

    # Save the chart to a file
    plt.savefig(pie_chart_filepath, dpi=300)
