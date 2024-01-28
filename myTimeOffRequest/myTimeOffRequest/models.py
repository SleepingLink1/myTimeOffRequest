from django.db import models
from django.contrib.auth.models import User

class TimeOffRequest(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"



class Employee(User):
    employee_id = models.CharField(max_length=100)
