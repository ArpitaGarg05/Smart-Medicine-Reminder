from django.urls import path

from medicines.views import (
    confirm_medicines_view,
    dashboard_view,
    mark_taken_view,
    medicine_add_view,
    medicine_delete_view,
    medicine_edit_view,
    medicines_list_view,
    shared_dashboard_view,
    toggle_taken_view,
)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('confirm/', confirm_medicines_view, name='confirm_medicines'),
    path('list/', medicines_list_view, name='medicines_list'),
    path('add/', medicine_add_view, name='medicine_add'),
    path('edit/<int:medicine_id>/', medicine_edit_view, name='medicine_edit'),
    path('delete/<int:medicine_id>/', medicine_delete_view, name='medicine_delete'),
    path('taken/<int:reminder_id>/', mark_taken_view, name='mark_taken'),
    path('shared/<int:owner_id>/dashboard/', shared_dashboard_view, name='shared_dashboard'),
    path('shared/<int:owner_id>/list/', medicines_list_view, name='shared_medicines_list'),
    path('toggle-taken/<int:schedule_id>/', toggle_taken_view , name='toggle_taken'),
]
