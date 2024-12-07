# Create your models here.
from django.db import models
from account.models import CustomUser
from .utils import relative_created_at


class Discussion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,db_column='author')
    category_list = [
        ('PPN_PPnBM', 'PPN dan PPnBM'),
        ('PPH_B', 'PPh Badan'),
        ('PPH_P', 'PPh Pemotongan/Pemungutan'),
        ('PPH_OP', 'PPh Orang Pribadi'),
        ('E_SPT', 'E-Spt'),
        ('PPH_21', 'PPh Pasal 21/26'),
        ('TA', 'Tax Amnesty'),
        ('AKP', 'Akuntansi Pajak'),
        ('PINT', 'Perpajakan Internasional'),
        ('BERITA', 'Bahas Berita'),
        ('PDRD', 'Pajak Daerah dan Retribusi Daerah'),
        ('PBB', 'Pajak Bumi dan Bangunan')
    ]
    category = models.CharField(max_length=255, choices=category_list)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def time_since(self):
        return relative_created_at(self.created_at)

    def __str__(self):
        return f'{self.user.username} - {self.category} - {relative_created_at(self.created_at)}: {self.content[:20]}...'

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='author')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def time_since(self):
        return relative_created_at(self.created_at)

    def __str__(self):
        return f'{self.user.username} - {relative_created_at(self.created_at)}: {self.content}'
