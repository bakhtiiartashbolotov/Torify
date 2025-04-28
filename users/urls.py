from django.urls import path, include

urlpatterns = [
    path('user_list/', include('users.urls')),
]