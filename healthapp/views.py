from django.shortcuts import render, redirect, get_object_or_404
from .models import PatientRecord
from .forms import PatientForm
from .services.gemini_service import generate_ai_remarks


def patient_list(request):
    records = PatientRecord.objects.all().order_by('-id')
    return render(request, 'healthapp/patient_list.html', {'records': records})


def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)

            # --- CALLING GEMINI AI HERE ---
            record.remarks = generate_ai_remarks(record.glucose, record.haemoglobin, record.cholesterol)

            record.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'healthapp/patient_form.html', {'form': form, 'action': 'Create'})


def patient_update(request, pk):
    record = get_object_or_404(PatientRecord, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)

            # --- RE-CALLING GEMINI AI ON UPDATE ---
            # We re-generate remarks in case the blood test values were changed
            record.remarks = generate_ai_remarks(record.glucose, record.haemoglobin, record.cholesterol)

            record.save()
            return redirect('patient_list')
    else:
        initial_data = {'date_of_birth': record.date_of_birth.strftime('%d/%m/%Y')}
        form = PatientForm(instance=record, initial=initial_data)

    return render(request, 'healthapp/patient_form.html', {'form': form, 'action': 'Update'})


def patient_delete(request, pk):
    record = get_object_or_404(PatientRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        return redirect('patient_list')
    return render(request, 'healthapp/patient_delete.html', {'record': record})

def refresh_all_remarks(request):
    records = PatientRecord.objects.all()
    for record in records:
        # Re-call AI for every record
        record.remarks = generate_ai_remarks(record.glucose, record.haemoglobin, record.cholesterol)
        record.save()
    return redirect('patient_list')