from datetime import datetime, timedelta
from accounts.models import Appointment 

class ConflictChecker:
    @staticmethod
    def has_conflicts(user, appointment_date, appointment_time, duration_minutes):
         # Update the import to match your project structure
        start_time = datetime.combine(appointment_date, appointment_time)
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        overlapping_appointments = Appointment.objects.filter(
            user=user,
            status__in=['pending', 'approved'],
            appointment_date=appointment_date,
            appointment_time__lt=end_time.time(),
            end_time__gt=start_time.time()
        )
        return overlapping_appointments.exists()