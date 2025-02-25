from django.db import models

    
class weekdays(models.Model):
    date=models.CharField(max_length=10)
    weekday=models.CharField(max_length=2)


