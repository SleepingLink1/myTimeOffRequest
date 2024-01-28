from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from .models import TimeOffRequest

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
