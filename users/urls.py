from django.urls import path

from users.views import register_view, revoke_caregiver_view, sharing_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('sharing/', sharing_view, name='sharing'),
    path('sharing/revoke/<int:access_id>/', revoke_caregiver_view, name='revoke_caregiver'),
]
