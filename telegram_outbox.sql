-- ksql query to create a stream for telegram bot outbox
CREATE STREAM telegram_outbox (
`chat_id` VARCHAR,
`text` VARCHAR
) WITH (
  KAFKA_TOPIC = 'telegram_outbox',
  PARTITIONS = 1,
  VALUE_FORMAT = 'avro'
 );