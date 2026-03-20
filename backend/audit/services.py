from audit.models import AuditEvent


def log_audit_event(*, tenant, actor, entity_type, entity_id, action, payload=None):
    return AuditEvent.objects.create(
        tenant=tenant,
        actor=actor,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        payload=payload or {},
    )