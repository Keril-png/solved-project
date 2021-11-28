from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Problem(models.Model):
    title = models.CharField(max_length = 64, verbose_name = 'title')
    description = models.TextField(verbose_name = 'description')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='date'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='problems', 
        verbose_name='author'
    ) 
    file = models.FileField(
        blank=True
    )
    
    def __str__(self):
        return self.title
    
