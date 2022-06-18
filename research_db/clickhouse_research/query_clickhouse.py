import time

from clickhouse_driver import Client


def mongo_connect():
    client = Client(host="clickhouse")

    movie_ids = [item[0] for item in client.execute("select distinct  movie_id from movies.likes limit 100")]

    print("---" * 20)
    print(f"Start read likes average score for 100 movies")
    all_times = []
    for movie in movie_ids:
        start_time = time.time()
        client.execute(f"select avg(score) from movies.likes where movie_id == '{movie}'")
        end_time = time.time() - start_time
        all_times.append(end_time)

    time_avg = sum(all_times) / len(all_times)
    print(f" Average time for read 1 movie average score {round(time_avg, 4)} second")
    print("---" * 20)

    print(f"Start read likes and dislikes count for 100 movies")
    all_times = []
    for movie in movie_ids:
        start_time = time.time()
        client.execute(
            f"select countIf(score = 10) as likes, countIf(score = 0) as dislikes from movies.likes where movie_id == '{movie}'"
        )
        end_time = time.time() - start_time
        all_times.append(end_time)

    time_avg = sum(all_times) / len(all_times)
    print(f" Average time for read 1 movie likes and dislikes count {round(time_avg, 4)} second")
    print("---" * 20)


if __name__ == "__main__":
    mongo_connect()
