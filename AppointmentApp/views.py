from django.shortcuts import render
from .models import Appointment

def mes_rendez_vous(request):
    patient = request.user.patient

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by('appointment_date')

    return render(
        request,
        'AppointmentApp/mes_rendez_vous.html',
        {'appointments': appointments}
    )