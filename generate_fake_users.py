from app.models import User
from app import app, db
from faker import Faker
import random

with app.app_context():
    fake = Faker()
    usernames = []
    for _ in range(995):

        name = "sponge bob"
        username = name.lower().replace(' ', '.')
        while username in usernames:
            name = fake.name()
            username = f"{name.lower().replace(' ', '.')}{random.randint(0, 999)}"
        usernames.append(username)

        user = User(
            username=username,
            email=fake.email()
        )
        # Assuming your User model has a set_password method
        user.set_password('defaultpassword')
        db.session.add(user)

    db.session.commit()
    print("done!")