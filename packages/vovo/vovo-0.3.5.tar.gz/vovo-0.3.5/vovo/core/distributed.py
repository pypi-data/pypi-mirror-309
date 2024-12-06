from celery import Celery
from vovo.settings import global_settings

celery_app = Celery(global_settings.CELERY_NAME, broker_url=global_settings.CELERY_BROKER,
                    backend=global_settings.CELERY_RESULT_BACKEND,
                    task_serializer=global_settings.CELERY_TASK_SERIALIZER,
                    result_serializer=global_settings.CELERY_TASK_SERIALIZER,
                    broker_transport_options={'visibility_timeout': 3600},  # 任务过期时间 1 hour
                    broker_connection_retry_on_startup=True
                    )
