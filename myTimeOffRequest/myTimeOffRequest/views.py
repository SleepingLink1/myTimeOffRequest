from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .models import TimeOffRequest
from django.shortcuts import render
from django.views import View


class LoginView(View):
    def get(self, request):
        # Render the login form
        return render(request, 'home.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse('Logged in successfully.')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse('Invalid username or password.')


class TimeOffRequestView(View):
    def get(self, request):
        return render(request, 'time_off_request.html')


@login_required
def modify_time_off_request(request, request_id):
    time_off_request = TimeOffRequest.objects.get(id=request_id)
    if request.user != time_off_request.user:
        return HttpResponseForbidden()
        # Get the new start and end dates from the form data
    new_start_date = request.POST.get('new_start_date')
    new_end_date = request.POST.get('new_end_date')
    user_requests = TimeOffRequest.objects.filter(user=request.user)
    for req in user_requests:
        if new_start_date < req.end_date and new_end_date > req.start_date:
            return HttpResponse('New request overlaps with an existing one.')
    time_off_request.start_date = new_start_date
    time_off_request.end_date = new_end_date
    time_off_request.save()
    # ...
    return HttpResponse('Request modified successfully.')
