from email.policy import default

from django.db import models

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default='Temp@123')


    def __str__(self):
        return self.full_name

class HealthRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='health_records'
    )
    glucose = models.DecimalField(max_digits=5,decimal_places=2)
    haemoglobin = models.DecimalField(max_digits=5, decimal_places=2)
    cholesterol = models.DecimalField(max_digits=5,decimal_places=2)
    remarks = models.CharField(max_length=255, blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)

