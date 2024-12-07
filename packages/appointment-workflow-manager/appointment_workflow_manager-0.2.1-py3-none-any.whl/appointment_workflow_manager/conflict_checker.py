from datetime import datetime, timedelta
from accounts.models import Appointment

class ConflictChecker:
    @staticmethod
    def has_conflicts(user, appointment_date, appointment_time, duration_minutes):
        """
        Check for overlapping appointments for the same user.
        """
        # Calculate start and end times of the new appointment
        start_time = datetime.combine(appointment_date, appointment_time)
        end_time = start_time + timedelta(minutes=duration_minutes)

        # Query overlapping appointments
        overlapping_appointments = Appointment.objects.filter(
            user=user,
            status__in=['pending', 'approved'],  # Check for active appointments
            appointment_date=appointment_date,
        ).filter(
            appointment_time__lt=end_time.time(),  # Overlapping start time
            appointment_time__gte=(start_time - timedelta(minutes=duration_minutes)).time()  # Overlapping end time
        )
        return overlapping_appointments.exists()
