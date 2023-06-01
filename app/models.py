from django.db import models
from datetime import date
# Create your models here.
class Students(models.Model):
    total = models.IntegerField()
    total_precent = models.IntegerField()
    total_absent = models.IntegerField()
    on_duty = models.IntegerField()
    date = models.DateField(default=date.today())

    def __str__(self):
        return "Students Counts"