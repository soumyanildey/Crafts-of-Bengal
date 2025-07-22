from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from login.models import UserProfile
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake users and their profiles'

    def handle(self, *args, **options):
        fake = Faker()
        users = []
        user_profiles = []
        existing_usernames = set()

        # Create 10k users
        for _ in range(1000):
            while True:
                username = fake.user_name()
                if username not in existing_usernames:  # Ensure unique usernames
                    existing_usernames.add(username)
                    break

            password = fake.password()
            email = fake.email()
            user = User(username=username, email=email)
            user.set_password(password)
            users.append(user)

            # Create user profile for each user
            user_profile = UserProfile(user=user, ph_no=int(''.join(filter(str.isdigit, fake.phone_number()))), gender=random.choice(['M', 'F', 'O']))
            user_profiles.append(user_profile)

        for user in users:
            user.save()  # Save the User object (this will trigger validation and related model signals)

        for profile in user_profiles:
            profile.save()  # Save the UserProfile object (this will link the profile to the user)
        
        self.stdout.write(self.style.SUCCESS('Successfully created fake users and profiles'))