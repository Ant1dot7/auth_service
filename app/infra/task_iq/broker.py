from taskiq_redis import ListQueueBroker


broker = ListQueueBroker(
    url="redis://redis:6379/0",
)
