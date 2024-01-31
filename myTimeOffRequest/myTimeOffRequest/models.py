from datetime import date
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
    employee_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



    def days_off_this_year(self):
        request_list = self.get_time_off_requests(self.employee_id)
        current_year = date.today().year
        total_days_off = 0
        for request in request_list.filter(start_date__year=current_year):
            total_days_off += (request.end_date - request.start_date).days + 1
        return total_days_off

    def get_time_off_requests(employee_id):
        employee = Employee.objects.get(employee_id=employee_id)
        time_off_requests = employee.timeoffrequest_set.all()
        return time_off_requests
