from django.apps import AppConfig
import redis
from dotenv import load_dotenv
import os

load_dotenv()

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'

    def ready(self):
        import posts.signals

red = redis.Redis(
    host=os.getenv('REDIS_ENDPOINT'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD')
)