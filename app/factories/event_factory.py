import factory
from faker import Faker
from app.models.models import Event, User
from app.database import SessionLocal

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    id = factory.Faker('uuid4')
    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    hashed_password = factory.LazyFunction(lambda: fake.password())

class EventFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Event
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    description = factory.LazyFunction(lambda: fake.text())
    start_date = factory.LazyFunction(lambda: fake.date_time_this_month(before_now=False, after_now=True))
    end_date = factory.LazyFunction(lambda: fake.date_time_this_month(before_now=False, after_now=True, start_date="+1d"))
    is_public = factory.LazyFunction(lambda: fake.boolean())
    creator = factory.SubFactory(UserFactory)
