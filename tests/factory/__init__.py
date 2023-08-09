import factory
from faker import Factory as FakerFactory
from pytest_factoryboy import register

from src.user.models import User, UserRoles

faker = FakerFactory.create()


@register
class UserFactory(factory.Factory):
    """User Factory"""

    class Meta:
        model = User

    firstname = factory.LazyFunction(faker.first_name)
    lastname = factory.LazyFunction(faker.last_name)
    image_url = factory.LazyFunction(faker.image_url)

    email = factory.LazyFunction(faker.safe_email)
    phone_number_country_code = "+1"
    phone_number = factory.LazyAttribute(
        lambda x: faker.pyint(999_999_999, 10_000_000_000)
    )

    password = factory.LazyFunction(faker.password)

    role = UserRoles.USER.value
    email_verified = True
    phone_number_verified = True

    created_by = "SYSTEM_ADMIN"
    updated_by = "SYSTEM_ADMIN"
