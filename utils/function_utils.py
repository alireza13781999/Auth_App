import random
from django.utils import timezone
from datetime import timedelta

def generate_verification_code():
    return str(random.randint(10000, 99999))

def check_ip_block(ip_address, model, attempt_limit=3, block_duration=1):
    block_time = timezone.now() - timedelta(hours=block_duration)
    return model.objects.filter(ip_address=ip_address, attempts__gte=attempt_limit, last_attempt__gte=block_time).exists()
