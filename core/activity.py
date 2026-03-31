from core.models import ActivityLog


def log_activity(*, actor, action, target_object=None, note=''):
    ActivityLog.objects.create(
        actor=actor,
        action=action,
        target_object=target_object,
        note=note,
    )

