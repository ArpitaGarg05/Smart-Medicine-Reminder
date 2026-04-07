from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import CaregiverInviteForm, RegisterForm
from users.models import CaregiverAccess


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'users/register.html', {'form': form})


@login_required
def sharing_view(request):
    form = CaregiverInviteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        caregiver = User.objects.filter(email__iexact=form.cleaned_data['caregiver_email']).first()
        if not caregiver:
            messages.error(request, 'No user found with this email.')
        elif caregiver == request.user:
            messages.error(request, 'You cannot add yourself.')
        else:
            CaregiverAccess.objects.get_or_create(owner=request.user, caregiver=caregiver)
            messages.success(request, 'Caregiver added.')
        return redirect('sharing')

    return render(
        request,
        'users/sharing.html',
        {
            'form': form,
            'my_caregivers': CaregiverAccess.objects.filter(owner=request.user).select_related('caregiver'),
            'shared_with_me': CaregiverAccess.objects.filter(caregiver=request.user).select_related('owner'),
        },
    )


@login_required
def revoke_caregiver_view(request, access_id):
    access = get_object_or_404(CaregiverAccess, id=access_id, owner=request.user)
    if request.method == 'POST':
        access.delete()
        messages.success(request, 'Caregiver access removed.')
    return redirect('sharing')
