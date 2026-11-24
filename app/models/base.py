from datetime import datetime
from ..extensions import db


class TimestampMixin:
    """Añade created_at y updated_at a cualquier modelo."""

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )