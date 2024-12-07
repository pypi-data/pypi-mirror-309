# Appointment Workflow Manager

`appointment-workflow-manager` is a Python package designed to simplify and standardize the management of appointment workflows in Django applications. It provides utilities for managing appointment approvals, rejections, cancellations, auditing status changes, and conflict detection.

---

## Features

- **Workflow Management**:
  - Approve, reject, or cancel appointments.
  - Automatically update appointment status and manage notifications.

- **Audit Logging**:
  - Log status changes of appointments with timestamps.
  - Helps maintain a historical record of changes for reporting and debugging.

- **Conflict Detection**:
  - Detect overlapping or conflicting appointments for the same user.
  - Prevent scheduling conflicts during appointment creation.

- **Reusable Logic**:
  - Encapsulates complex business logic into a reusable package for modular and maintainable code.

---

## Installation

To install the package, use `pip`:

```bash
pip install appointment-workflow-manager
```
## Usage

### 1. Workflow Management

The `AppointmentWorkflowManager` class simplifies appointment workflows such as approval, rejection, and cancellation.

#### Approving an Appointment
```python
from appointment_workflow_manager.workflow_manager import AppointmentWorkflowManager

appointment = Appointment.objects.get(id=1)  # Fetch an appointment instance
AppointmentWorkflowManager.approve(appointment)
```

```python
from appointment_workflow_manager.workflow_manager import AppointmentWorkflowManager

appointment = Appointment.objects.get(id=1)  # Fetch an appointment instance
AppointmentWorkflowManager.reject(appointment, "Customer unavailable")
```

```python
from appointment_workflow_manager.workflow_manager import AppointmentWorkflowManager

appointment = Appointment.objects.get(id=1)  # Fetch an appointment instance
AppointmentWorkflowManager.cancel(appointment)
```

###Conflict Detection
####The ConflictChecker class detects overlapping or conflicting appointments.
####Checking for Appointment Conflicts

```python
from appointment_workflow_manager.conflict_checker import ConflictChecker

# Appointment details
appointment_date = datetime.date(2024, 11, 20)
appointment_time = datetime.time(10, 0)  # 10:00 AM
duration_minutes = 60  # 1-hour duration

# Check for conflicts
if ConflictChecker.has_conflicts(user=request.user, appointment_date=appointment_date, appointment_time=appointment_time, duration_minutes=duration_minutes):
    print("Conflict detected! Please choose another time.")
else:
    print("No conflicts. Proceed with appointment creation.")
```


###Audit Logging
####The AuditLogger class tracks changes in appointment statuses for historical records or debugging.

####Logging Status Changes

```python
from appointment_workflow_manager.audit_logger import AuditLogger

# Log a status change for an appointment
AuditLogger.log_status_change(
    user=request.user, 
    appointment=appointment, 
    old_status="pending", 
    new_status="approved"
)
```