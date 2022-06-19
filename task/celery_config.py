## Broker settings.
broker_url = 'amqp://root:root@rabbitmq//'

# List of modules to import when the Celery worker starts.
imports = ('task.workers',)

## Using the database to store task state and results.
result_backend = 'redis://redis:6379/0'
#result_persistent = False

accept_content = ['json', 'application/text']

result_serializer = 'json'
timezone = "UTC"
