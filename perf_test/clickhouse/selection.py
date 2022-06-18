import time
from pathlib import Path

import pandas as pd
from clickhouse_driver import Client

DATA_PATH = Path("../test_data.csv").resolve()

click_client = Client(host="localhost", port=9000)

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    times = []
    for column in df.columns:
        column_times = []
        for _ in range(20):
            value = df[column].sample(n=1).values[0]

            t0 = time.monotonic()
            click_client.execute(f"select * from test.test_table where {column} == %(value)s", {"value": value})
            column_times.append(time.monotonic() - t0)

        times.append(sum(column_times) / len(column_times))
        print(f"Mean selection duration for {column} {sum(column_times) / len(column_times)}")
        print(f"Total selection duration for {column} {sum(column_times)} of {len(column_times)} records")

    print(f"Mean selection duration {sum(times) / len(times)}")
