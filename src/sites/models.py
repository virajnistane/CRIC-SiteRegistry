from django.db import models # type: ignore

# Create your models here.

class Site(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('degraded', 'Degraded'),
    ]

    name = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    cpu_capacity = models.IntegerField(help_text='Total CPU cores')
    storage_tb = models.FloatField(help_text='Total storage in TB')

    def __str__(self):
        return self.name