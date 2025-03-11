import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from core.models import Tweet

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake tweets'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of tweets to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        users = list(User.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('No users found. Create some users first.'))
            return

        tweets = []
        for _ in range(count):
            user = random.choice(users)
            text = fake.sentence(nb_words=20)

            tweet = Tweet(
                user=user,
                text=text
            )
            tweets.append(tweet)

        # Bulk create for efficiency
        Tweet.objects.bulk_create(tweets)

        self.stdout.write(self.style.SUCCESS(f"{count} tweets created successfully!"))
