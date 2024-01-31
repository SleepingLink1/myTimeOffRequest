"""
URL configuration for myTimeOffRequest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import base_redirect, EmployeeRegistrationView, UserTimeOffRequestsView, HomeView, TimeOffRequest, ModifyTimeOffRequest
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_redirect, name='base_redirect'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', EmployeeRegistrationView.as_view(), name='signup'),
    path('home', HomeView, name='home'),
    path('submit_new_request/', TimeOffRequest, name='submit_new_request'),
    path('modify_request/', ModifyTimeOffRequest, name='modify_request'),
    path('time_off_requsts/<int:request_id>/', UserTimeOffRequestsView, name='time_off_requests'),
    path('delete_request/<int:request_id>/', UserTimeOffRequestsView, name='delete_request'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
