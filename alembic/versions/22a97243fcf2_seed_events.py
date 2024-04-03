"""seed events

Revision ID: 22a97243fcf2
Revises: 089b3ac22c5d
Create Date: 2024-04-03 04:15:09.562509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22a97243fcf2'
down_revision: Union[str, None] = '089b3ac22c5d'
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



def downgrade() -> None:
    pass
