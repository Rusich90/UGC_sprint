import random
from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from faker import Faker
from tqdm import tqdm

fake = Faker()


def generate(*args, **kwargs) -> Dict[str, Any]:
    return {
        "name": fake.name(),
        "address": fake.address(),
        "phone": fake.phone_number(),
        "jon": fake.job(),
        "age": random.randint(18, 80),
        "company": fake.company(),
        "card": fake.credit_card_number(),
    }


def generate_n(n: int) -> List[Dict[str, Any]]:
    with Pool(cpu_count()) as p:
        data = p.map(generate, range(n))
    return data


if __name__ == "__main__":
    save_path = Path("test_data.csv")

    for i in tqdm(range(10)):
        batch = generate_n(1000000)
        df = pd.DataFrame.from_records(batch)

        if save_path.exists():
            prev_df = pd.read_csv(save_path)
            df = pd.concat([prev_df, df])

        df.to_csv(save_path, index=False)
