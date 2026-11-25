
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient, Specialty


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Informations personnelles',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                )
            }
        ),
    )


admin.site.register(Specialty)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'license_number')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('license_number',)
        return ()


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'national_id')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('national_id',)
        return ()
