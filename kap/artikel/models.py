from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from account.models import CustomUser
# Create your models here.

#model database
# judul, konten, img, deskripsi, nama penulis, tanggal publish


# class Status(models.TextChoices):
#     DRAFT = 'draft', 'Draft'
#     PUBLISHED = 'published', 'Published'
#     ARCHIVED = 'archived', 'Archived'

class Artikel(models.Model):
    title= models.CharField('Judul',max_length=50)
    description= models.TextField('Deskripsi')
    image= models.ImageField('Gambar',upload_to='artikel/')
    content= CKEditor5Field(config_name='article', null=True, blank=True)
    published_at= models.DateTimeField('Waktu Publish', null=True, blank=True)
    created_at= models.DateTimeField('Waktu Buat',auto_now_add=True)
    updated_at= models.DateTimeField('Waktu Update', null=True, blank=True)
    deleted_at= models.DateTimeField('Waktu Hapus',null=True,blank=True)
    draft_for = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='draft'
    )
    # status= models.CharField('Status',choices=Status.choices,default=Status.DRAFT, max_length=10)
    # For status, use published_at and deleted_at, published_at is null if not published, deleted_at is null if not deleted, published_at more than current time means not published yet.
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='artikel_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='artikel_updated')

class ContentMedia(models.Model):
    artikel = models.ForeignKey(Artikel, on_delete=models.CASCADE, related_name='content_media')
    file = models.CharField('File Path', max_length=255, help_text='Path to the file in S3 storage')
    created_at= models.DateTimeField('Waktu Buat',auto_now_add=True)
    deleted_at= models.DateTimeField('Waktu Hapus',null=True,blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='content_media_created')

    def __str__(self):
        return f"{self.artikel.title} - {self.file.name}"