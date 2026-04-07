from django.urls import path

from prescriptions.views import parsed_debug_view, upload_prescription_view

urlpatterns = [
    path('upload/', upload_prescription_view, name='upload_prescription'),
    path('parsed/<int:prescription_id>/', parsed_debug_view, name='parsed_debug'),
]
