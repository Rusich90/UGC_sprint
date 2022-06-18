import time
from pathlib import Path

import pandas as pd
import vertica_python

DATA_PATH = Path("../test_data.csv").resolve()


conn_info = {"host": "localhost", "port": 5433, "user": "dbadmin", "password": "", "database": "VMart"}
cur = vertica_python.connect(**conn_info).cursor()


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    times = []
    for column in df.columns:
        column_times = []
        for _ in range(20):
            value = df[column].sample(n=1).values[0]

            t0 = time.monotonic()
            cur.execute(f"SELECT * FROM test_table WHERE {column} = :value", {"value": str(value)})
            column_times.append(time.monotonic() - t0)

        times.append(sum(column_times) / len(column_times))
        print(f"Mean selection duration for {column} {sum(column_times) / len(column_times)}")
        print(f"Total selection duration for {column} {sum(column_times)} of {len(column_times)} records")

    print(f"Mean selection duration {sum(times) / len(times)}")
