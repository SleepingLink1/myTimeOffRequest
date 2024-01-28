from django.db import models


class TimeOffRequest(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"

    class Employee(models.Model):
        employeeID = models.CharField(max_length=200, unique=True)
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.EmailField()

        def __str__(self):
            return f"{self.first_name} {self.last_name} ({self.employeeID})"
