from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from medicines.forms import MedicineConfirmFormSet, MedicineEditForm
from medicines.models import Medicine
from prescriptions.models import Prescription
from reminders.models import Reminder
from reminders.services import generate_today_reminders
from users.models import CaregiverAccess
from reminders.services import create_reminders
from .models import MedicineSchedule
from datetime import datetime
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

def _resolve_target(request, owner_id=None):
    if owner_id is None:
        return request.user, True
    owner = get_object_or_404(User, id=owner_id)
    if CaregiverAccess.objects.filter(owner=owner, caregiver=request.user).exists():
        return owner, False
    return None, False


@login_required
def dashboard_view(request):
    user, can_edit = _resolve_target(request)

    today_day = datetime.today().strftime('%A').lower()

    medicines = Medicine.objects.filter(user=user).prefetch_related('schedules')

    today_meds = []

    for med in medicines:

        # DAILY
        if med.frequency_type == 'daily':
            for schedule in med.schedules.all():
                today_meds.append({
                    'id': schedule.id, 
                    'name': med.name,
                    'dosage': med.dosage,
                    'time': schedule.time,
                    'taken': schedule.is_taken_today(),
                    'remaining': med.remaining_quantity
                })

        # WEEKLY
        elif med.frequency_type == 'weekly':
            if med.day_of_week and med.day_of_week.lower() == today_day:
                for schedule in med.schedules.all():
                    today_meds.append({
                        'name': med.name,
                        'dosage': med.dosage,
                        'time': schedule.time,
                        'remaining': med.remaining_quantity
                    })

    # 🔥 SORT BY TIME
    today_meds.sort(key=lambda x: x['time'])

    low_stock = [m for m in user.medicines.all() if m.is_low_stock]

    return render(request, 'medicines/dashboard.html', {
        'today_meds': today_meds,
        'low_stock_medicines': low_stock,
        'can_edit': can_edit,
        'target_user': user
    })


@login_required
def shared_dashboard_view(request, owner_id):
    user, can_edit = _resolve_target(request, owner_id)
    if not user:
        messages.error(request, 'Unauthorized')
        return redirect('sharing')

    today_day = datetime.today().strftime('%A').lower()

    medicines = Medicine.objects.filter(user=user).prefetch_related('schedules')

    today_meds = []

    for med in medicines:

        if med.frequency_type == 'daily':
            for schedule in med.schedules.all():
                today_meds.append({
                    'name': med.name,
                    'dosage': med.dosage,
                    'time': schedule.time,
                    'remaining': med.remaining_quantity
                })

        elif med.frequency_type == 'weekly':
            if med.day_of_week and med.day_of_week.lower() == today_day:
                for schedule in med.schedules.all():
                    today_meds.append({
                        'name': med.name,
                        'dosage': med.dosage,
                        'time': schedule.time,
                        'remaining': med.remaining_quantity
                    })

    today_meds.sort(key=lambda x: x['time'])

    low_stock = [m for m in user.medicines.all() if m.is_low_stock]

    return render(request, 'medicines/dashboard.html', {
        'today_meds': today_meds,
        'low_stock_medicines': low_stock,
        'can_edit': can_edit,
        'target_user': user
    })


@login_required
def confirm_medicines_view(request):
    pid = request.session.get('pending_prescription_id')
    if not pid:
        return redirect('upload_prescription')

    prescription = get_object_or_404(Prescription, id=pid, user=request.user)
    initial = prescription.ai_parsed_data or [{}]

    # ✅ FIXED FORMSET HANDLING
    if request.method == 'POST':
        formset = MedicineConfirmFormSet(request.POST)
    else:
        formset = MedicineConfirmFormSet(initial=initial)

    # ✅ DEBUG (you can remove later)
    if request.method == 'POST':
        from reminders.services import create_reminders

        print("FORM VALID:", formset.is_valid())
        print("ERRORS:", formset.errors)

        for form in formset:
            if not form.cleaned_data:
                continue

            name = form.cleaned_data.get('name', '').strip()

        # 🔥 SKIP EMPTY ROWS
            if not name:
                continue

            if form.cleaned_data.get('delete'):
                continue

            qty = form.cleaned_data.get('total_quantity') or 1

            medicine = Medicine.objects.create(
                user=request.user,
                name=name,
                dosage=form.cleaned_data.get('dosage', ''),
                total_quantity=qty,
                remaining_quantity=qty,
            )

            create_reminders(medicine)

        request.session.pop('pending_prescription_id', None)
        return redirect('medicines_list')

             #CREATE REMINDERS
        create_reminders(medicine)

        request.session.pop('pending_prescription_id', None)
        return redirect('medicines_list')

    return render(request, 'medicines/confirm.html', {
        'formset': formset,
        'prescription': prescription
    })


@login_required
def medicines_list_view(request, owner_id=None):
    user, can_edit = _resolve_target(request, owner_id)
    if not user:
        messages.error(request, 'Unauthorized')
        return redirect('sharing')
    medicines = Medicine.objects.filter(user=user)
    return render(request, 'medicines/list.html', {'medicines': medicines, 'can_edit': can_edit, 'target_user': user})




@login_required
def medicine_edit_view(request, medicine_id):
    med = get_object_or_404(Medicine, id=medicine_id, user=request.user)
    form = MedicineEditForm(request.POST or None, instance=med)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('medicines_list')
    return render(request, 'medicines/edit.html', {'form': form})


@login_required
def medicine_delete_view(request, medicine_id):
    med = get_object_or_404(Medicine, id=medicine_id, user=request.user)
    if request.method == 'POST':
        med.delete()
    return redirect('medicines_list')


@login_required
def mark_taken_view(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.taken = True
    reminder.save(update_fields=['taken'])
    return redirect('dashboard')


@login_required
def medicine_add_view(request):
    form = MedicineEditForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        med = form.save(commit=False)
        med.user = request.user
        med.save()

        # 🔥 STEP 2: SAVE MULTIPLE TIMES
        times = request.POST.getlist('times[]')

        for t in times:
            if t:
                MedicineSchedule.objects.create(
                    medicine=med,
                    time=t
                )

        return redirect('medicines_list')

    return render(request, 'medicines/add.html', {'form': form})


from django.utils.timezone import now

@login_required
def toggle_taken_view(request, schedule_id):
    schedule = get_object_or_404(MedicineSchedule, id=schedule_id, medicine__user=request.user)

    today = now().date()

    if schedule.last_taken_date == today:
        # 🔄 UNDO
        schedule.last_taken_date = None
        schedule.medicine.remaining_quantity += 1
    else:
        # ✅ MARK
        schedule.last_taken_date = today
        schedule.medicine.remaining_quantity -= 1

    schedule.medicine.save()
    schedule.save()

    return redirect('dashboard')