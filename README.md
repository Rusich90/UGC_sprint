# [Проектная работа 8 спринта](https://github.com/EgShes/ugc_sprint_1)

# Разработка

В проекте используется python3.9

## Прекоммит хуки

Прекоммит хуки автоматически запускаются перед коммитом и форматируют код. После того, как они отработали по комманде
`git commit` добавьте внесенные ими изменения `git add ...` и повторите `git commit`

Установка:
```bash
pip install pre-commit
pre-commit install
```

## ETL

Команда для первого запуска с настройками баз данных в кликхаусе:
```bash
make first-up
```

Команда для обычных запусков когда базы уже созданы:
```bash
docker-compose up
```

ЭТЛ логи:
```bash
make logs-etl
```

Зайти в Clickhouse консоль:
```bash
make console-clickhouse
```

В config/config.yaml можно настроить бэкофф для кафки, количество строк для сбора и отправки в кликхаус, а также LOG_LEVEL
