
from kap.storages import PrivateS3Storage
import threading


class CKEditor5Storage(PrivateS3Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location += '/artikel/content_media'