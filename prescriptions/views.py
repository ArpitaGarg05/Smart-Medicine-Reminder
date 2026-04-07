from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from prescriptions.forms import PrescriptionUploadForm
from prescriptions.models import Prescription
from prescriptions.services import extract_text_from_image, parse_prescription


@login_required
def upload_prescription_view(request):
    form = PrescriptionUploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        prescription = form.save(commit=False)
        prescription.user = request.user
        prescription.save()
        try:
            prescription.extracted_text = extract_text_from_image(prescription.image.path)
            prescription.ai_parsed_data = parse_prescription(prescription.extracted_text)
            prescription.save()
            request.session['pending_prescription_id'] = prescription.id
            return redirect('confirm_medicines')
        except Exception as exc:
            messages.error(request, f'Parsing failed: {exc}')
    return render(request, 'prescriptions/upload.html', {'form': form})


@login_required
def parsed_debug_view(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id, user=request.user)
    return render(request, 'prescriptions/parsed_debug.html', {'prescription': prescription})


