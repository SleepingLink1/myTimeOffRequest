from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .models import TimeOffRequest, Employee
from django.shortcuts import render
from django.views import View



def post(self, request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    employee_id = request.POST['employee_id']
    password = request.POST['password']
    if Employee.objects.filter(first_name=first_name, last_name=last_name).exists():
        return HttpResponse('A user with this first and last name already exists.')
    else:
        user = Employee.objects.create_user(username=employee_id, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return render(request, 'home.html')
class login_view(View):
    def get(self, request):
        # Render the login form
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return render(request, 'home.html')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('Invalid username or password.')

@login_required
def post(self, request):
    employee_id = request.POST['employee_id']
    password = request.POST['password']
    user = authenticate(request, username=employee_id, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'home.html')
    else:
        return HttpResponse('Invalid employee ID or password.')

@login_required
class home_view(View):
    def get(self, request):
        return render(request, 'home.html')
    def post(self, request):
        return render(request, 'home.html')

@login_required
class time_off_request(View):
    def get(self, request):
        return render(request, 'submit_new_request.html')
    def post(self, request, employee):
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        reason = request.POST['reason']
        user_requests = TimeOffRequest.objects.filter(user=request.user)
        new_request_days = (end_date - start_date).days + 1
        for req in user_requests:
            if employee.days_off_this_year() + new_request_days > 10 or start_date < req.end_date and \
                    end_date > req.start_date or start_date < date.today() or end_date < date.today():
                return HttpResponse('There was an error processing your request.')
        time_off_request.start_date = start_date
        time_off_request.end_date = end_date
        time_off_request.reason = reason
        time_off_request.save()
        return HttpResponse('Request created successfully.')


@login_required
def modify_time_off_request(request, request_id, employee):
    time_off_request = TimeOffRequest.objects.get(id=request_id)
    if request.user != time_off_request.user:
        return HttpResponseForbidden()
    new_start_date = request.POST.get('new_start_date')
    new_end_date = request.POST.get('new_end_date')
    user_requests = TimeOffRequest.objects.filter(user=request.user)
    new_request_days = (new_end_date - new_start_date).days + 1
    for req in user_requests:
        if employee.days_off_this_year() + new_request_days > 10 or new_start_date < req.end_date and new_end_date > req.start_date or new_start_date < date.today() or new_end_date < date.today():
            return HttpResponse('There was an error processing your request.')
    time_off_request.start_date = new_start_date
    time_off_request.end_date = new_end_date
    time_off_request.save()
    # ...
    return HttpResponse('Request modified successfully.')
