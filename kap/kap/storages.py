from storages.backends.s3boto3 import S3Boto3Storage
from django.urls import reverse
from urllib.parse import quote
import hashlib
import time
import os

class PrivateS3Storage(S3Boto3Storage):
    location = 'uploads' 
    default_acl = None  # (default ACL 'private' R2)

    def url(self, name):
        return reverse('media_proxy') + f'?key={quote(self.location + "/" + name)}'
    
    def get_available_name(self, name, max_length=None):
        # Pisahin nama dan ekstensi
        base, ext = os.path.splitext(name)

        # Hash timestamp
        timestamp = str(time.time()).encode('utf-8')
        hash_digest = hashlib.sha256(timestamp).hexdigest()[:8]  # 8 karakter cukup

        # Bangun nama baru
        name = f"{base}_{hash_digest}{ext}"

        # Pastikan tidak overwrite
        return super().get_available_name(name, max_length=max_length)