from datetime import datetime

class AppointmentWorkflowManager:
    @staticmethod
    def approve(appointment):
        if appointment.status != 'pending':
            raise ValueError("Only pending appointments can be approved.")
        appointment.status = 'approved'
        appointment.rejection_reason = None
        appointment.updated_at = datetime.now()
        appointment.save()

    @staticmethod
    def reject(appointment, rejection_reason):
        if appointment.status != 'pending':
            raise ValueError("Only pending appointments can be rejected.")
        if not rejection_reason:
            raise ValueError("Rejection reason is required.")
        appointment.status = 'rejected'
        appointment.rejection_reason = rejection_reason
        appointment.updated_at = datetime.now()
        appointment.save()

    @staticmethod
    def cancel(appointment):
        if appointment.status not in ['pending', 'approved']:
            raise ValueError("Only pending or approved appointments can be canceled.")
        appointment.status = 'canceled'
        appointment.updated_at = datetime.now()
        appointment.save()
