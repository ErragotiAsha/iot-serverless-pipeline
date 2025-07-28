SELECT
  sensor_id,
  zone,
  temperature,
  humidity,
  air_quality_index,
  timestamp
FROM clean
ORDER BY timestamp DESC
LIMIT 10;
