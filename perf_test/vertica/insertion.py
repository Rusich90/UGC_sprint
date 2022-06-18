import time
from pathlib import Path
from typing import Any, Dict, Iterator, List

import pandas as pd
import vertica_python
from verticapy import insert_into

DATA_PATH = Path("../test_data.csv").resolve()
BATCH = 10000
conn_info = {"host": "localhost", "port": 5433, "user": "dbadmin", "password": "", "database": "VMart"}
cur = vertica_python.connect(**conn_info).cursor()


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    data: Iterator[List[Dict[str, Any]]] = (
        df.iloc[int(i * BATCH) : int((i + 1) * BATCH)].values.tolist() for i in range(len(df) // BATCH)
    )

    times = []
    for batch in data:
        t0 = time.monotonic()
        insert_into(
            table_name="public.test_table",
            column_names=["name", "address", "phone", "jon", "age", "company", "card"],
            data=batch,
            cursor=cur,
        )
        times.append(time.monotonic() - t0)
        print(times[-1])

    print(f"Mean insertion duration {sum(times) / len(times)}")
    print(f"Total insertion duration {sum(times)} of {len(df)} records")
