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
# worker_pool = "eventlet"
# Worker có thể restart pool
worker_pool_restarts = True
# Khi xảy ra lỗi (như worker break) thì message sẽ được lưu trữ lại trong message queue
task_acks_late = True
# khi message được chạy lại thì status sẽ update thành STARTED
task_track_started = True
