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

# worker_pool = "threads"
# Worker có thể restart pool
worker_pool_restarts = True
# Khi xảy ra lỗi (như worker break) thì message sẽ được lưu trữ lại trong message queue
task_acks_late = True
# khi message được chạy lại thì status sẽ update thành STARTED
task_track_started = True

# giữ nguyên connection đang mở nếu broker_heartbeat = None
broker_heartbeat = None
# broker_heartbeat = 10
# broker_heartbeat_checkrate = 5

# Số lượng kết nối tối đa có thể mở trong pool connection
# các kết nối sẽ mở và đóng luôn sau mỗi lần sử dụng nếu broker_pool_limit = None
broker_pool_limit = None
# khi task chuyển trạng thái thì sẽ gửi state đến monitoring(flower)
worker_send_task_events = True
# Will delete all celeryev. queues without consumers after 1 minute.
event_queue_expires = 60

# concurrent connection need = broker_pool_limit * (web dynos * web workers + worker dynos * worker concurrency)
