from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse
from .models import TimeOffRequest, Employee
from django.shortcuts import render
from django.views import View


class EmployeeRegistrationView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        employee_id = request.POST['employee_id']
        password = request.POST['password']
        if Employee.objects.filter(first_name=first_name, last_name=last_name).exists():
            return HttpResponse('A user with this first and last name already exists.')
        else:
            user = Employee.objects.create_user(username=employee_id, password=password, first_name=first_name,
                                                last_name=last_name)
            login(request, user)
            return render(request, 'home.html')


class LoginView(View):
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
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request, message=None):
        return render(request, 'home.html', {message})


@login_required
class TimeOffRequest(View):
    def get(self, request):
        return render(request, 'submit_new_request.html')

    def post(self, request, employee):

        start_date = request.POST['start_date']
        is_valid = validate_request(request, employee)
        if is_valid:
            return render(request, 'home.html')
        else:
            return render(request, 'Home.html', {'error': 'There was an error processing your request.'})


@login_required
class ModifyTimeOffRequest(LoginRequiredMixin, View):
    def post(self, request, request_id, employee):
        new_request = request.objects.get(id=request_id)
        is_valid_request = validate_request(new_request, employee)
        if is_valid_request:
            render(request, 'home.html')
        else:
            render(request, 'home.html', {'error': 'There was an error processing your request.'})


def validate_request(request, employee):
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    reason = request.POST['reason']
    user_requests = TimeOffRequest.objects.filter(user=request.user)
    new_request_days = (end_date - start_date).days + 1
    for req in user_requests:
        if employee.days_off_this_year() + new_request_days > 10 or start_date < req.end_date and end_date > req.start_date or start_date < date.today() or end_date < date.today():
            return False
    user_requests.start_date = start_date
    user_requests.end_date = end_date
    user_requests.reason = reason
    user_requests.save()
    return True
