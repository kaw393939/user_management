import factory
from faker import Faker
from app.models import Event
from database import SessionLocal

fake = Faker()

class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = SessionLocal()  # Use your SQLAlchemy session here
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    description = factory.LazyFunction(lambda: fake.text())
    start_date = factory.LazyFunction(lambda: fake.date_time())
    end_date = factory.LazyFunction(lambda: fake.date_time_between(start_date="+1d", end_date="+30d"))
