import time
from pathlib import Path
from typing import Any, Dict, Iterator, List

import pandas as pd
from clickhouse_driver import Client

DATA_PATH = Path("../test_data.csv").resolve()
BATCH = 10000


click_client = Client(host="localhost", port=9000)


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)
    data: Iterator[List[Dict[str, Any]]] = (
        df.iloc[int(i * BATCH) : int((i + 1) * BATCH)].to_dict("records") for i in range(len(df) // BATCH)
    )

    times = []
    for batch in data:
        t0 = time.monotonic()
        click_client.execute(
            "INSERT INTO test.test_table (name, address, phone, jon, age, company, card) VALUES", batch
        )
        times.append(time.monotonic() - t0)
        print(times[-1])

    print(f"Mean insertion duration {sum(times) / len(times)}")
    print(f"Total insertion duration {sum(times)} of {len(df)} records")
