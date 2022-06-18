
# Perf test

| Database    | Insertion, sec | Selection no load, sec | Selection with load, sec |
|-------------|----------------|------------------------|--------------------------|
| Clickhouse* | 0.0359         | 0.0291                 | 0.0988                   |
| Vertica**   | 0.2718         | 0.0452                 | 0.0671                   |

* Clickhouse insertion time is reported for batches of 10000. Configuration - one shard, no replicas
** Vertica insertion time is reported for batches of 10000. Configuration - one shard, no replicas
