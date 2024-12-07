import datetime
from accounts.models import AuditLog

class AuditLogger:
    @staticmethod
    def log_status_change(appointment, old_status, new_status):
        AuditLog.objects.create(
            appointment=appointment,
            old_status=old_status,
            new_status=new_status,
            timestamp=datetime.now()
        )
