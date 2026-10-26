from django.db import models

class PatientRecord(models.Model):
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    email = models.EmailField()
    glucose = models.FloatField()
    haemoglobin = models.FloatField()
    cholesterol = models.FloatField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name