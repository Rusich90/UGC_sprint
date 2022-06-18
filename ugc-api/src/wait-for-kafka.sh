set -e
echo "Kafka broker is up - executing command222"
until kafkacat -b broker:9092 -L; do
  echo "Kafka broker is unavailable - sleeping"
  sleep 1
done

echo "Kafka broker is up - executing command"
exec uvicorn main:app --host=0.0.0.0 --port=8000
