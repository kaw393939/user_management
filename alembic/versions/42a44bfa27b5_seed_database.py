"""Seed database

Revision ID: 42a44bfa27b5
Revises: 1f04798b9a3a
Create Date: 2024-04-02 00:17:02.217433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42a44bfa27b5'
down_revision: Union[str, None] = '1f04798b9a3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Now, import your factory
from app.factories.event_factory import EventFactory  # Update this import path as necessary
from app.factories.event_factory import EventFactory  # Correct import path
from sqlalchemy.orm import Session
from database import Base, engine  # Assuming your engine is defined here

def upgrade():
    # Bind the session from your factory to Alembic's connection for the transaction
    Base.metadata.bind = engine

    # Create a session bound to the engine
    session = Session(bind=op.get_bind())

    # Assuming EventFactory is expecting a session, not session factory
    EventFactory._meta.sqlalchemy_session = session

    # If your EventFactory setup is different and needs adjustment,
    # make sure it's compatible with how you're creating the session here.

    # Generate and insert events
    for _ in range(100):  # Example: Generate 10 events
        EventFactory.create()

    session.commit()  # Don't forget to commit the session
    session.close()  # Cleanup the session after committing

def downgrade():
    # Implement your downgrade functionality here
    # This may involve deleting the seeded events or leaving it if it's not critical
    pass
