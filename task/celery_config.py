## Broker settings.
broker_url = 'amqp://root:root@rabbitmq//'

# List of modules to import when the Celery worker starts.
imports = ('task.workers',)

## Using the database to store task state and results.
result_backend = 'redis://redis:6379/0'
#result_persistent = False

accept_content = ['json', 'application/text']

result_serializer = 'json'
timezone = "Asia/Ho_Chi_Minh"

# worker_concurrency = 6
# worker_pool = "threads"
# Worker có thể restart pool
worker_pool_restarts = True
# Khi xảy ra lỗi (như worker break) thì message sẽ được lưu trữ lại trong message queue
task_acks_late = True
# khi message được chạy lại thì status sẽ update thành STARTED
task_track_started = True

broker_heartbeat = None
# broker_heartbeat = 10
# broker_heartbeat_checkrate = 5

# Số lượng kết nối tối đa có thể mở trong pool connection
# Setting BROKER_POOL_LIMIT to None disables pooling
# Disabling pooling causes open/close connections for every task.
# However, the rabbitMQ cluster being behind an Elastic Load Balancer,
# the pooling is not working correctly,
# and the connection is lost at some point.
# There seems no other way around it for the time being.
broker_pool_limit = None
# usage for monitoring(flower)
worker_send_task_events = True
# Will delete all celeryev. queues without consumers after 1 minute.
event_queue_expires = 60
