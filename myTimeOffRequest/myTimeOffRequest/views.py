from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from .models import TimeOffRequest, Employee
from django.shortcuts import render, redirect
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
            return render(request, 'signup.html', {'error': 'A user with this first and last name already exists.'})
        else:
            user = Employee.objects.create_user(username=employee_id, password=password, first_name=first_name,
                                                last_name=last_name)
            login(request, user)
            return render(request, 'home.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return render(request, 'home.html')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'home.html',{'error':'Invalid username or password.'})


@login_required
class HomeView(View):
    def get(self, request):
        if 'user_id' not in request.session:  # Check if user ID exists in session
            return redirect('login')
        return render(request, 'home.html')


@login_required
class TimeOffRequest(View):
    def get(self, request):
        return render(request, 'submit_new_request.html')

    def post(self, request):
        employee = Employee.objects.get(id=request.session['user_id'])
        is_valid = validate_request(request, employee)
        if is_valid:
            return render(request, 'home.html')
        else:
            return render(request, 'home.html', {'error': 'There was an error processing your request.'})


@login_required
class ModifyTimeOffRequest(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'time_off_requests.html')
    def post(self, request, request_id, employee):
        new_request = request.objects.get(id=request_id)
        is_valid_request = validate_request(new_request, employee)
        if is_valid_request:
            render(request, 'home.html')
        else:
            render(request, 'home.html', {'error': 'There was an error processing your request.'})


@login_required
class UserTimeOffRequestsView(LoginRequiredMixin, View):
    def get(self, request):
        user_requests = TimeOffRequest.objects.filter(user=request.user)
        return render(request, 'time_off_requests.html', {'time_off_requests': user_requests})

@login_required
class DeleteTimeOffRequestView(LoginRequiredMixin, View):
    def post(self, request, request_id):
        time_off_request = TimeOffRequest.objects.get(id=request_id)
        if request.user == time_off_request.user:
            time_off_request.delete()
        return redirect(reverse('home.html'))
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

def base_redirect(request):
    return redirect('login')
