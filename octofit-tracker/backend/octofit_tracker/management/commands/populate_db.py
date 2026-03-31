from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.conf import settings
import pymongo

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear all data
        Activity.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', universe='Marvel')
        dc = Team.objects.create(name='DC', universe='DC')

        # Create Users
        users = [
            User.objects.create(email='tony@stark.com', name='Tony Stark', team=marvel, is_leader=True),
            User.objects.create(email='steve@rogers.com', name='Steve Rogers', team=marvel),
            User.objects.create(email='bruce@wayne.com', name='Bruce Wayne', team=dc, is_leader=True),
            User.objects.create(email='clark@kent.com', name='Clark Kent', team=dc),
        ]

        # Create Activities
        Activity.objects.create(user=users[0], type='Iron Suit Training', duration=60, date=timezone.now())
        Activity.objects.create(user=users[1], type='Shield Practice', duration=45, date=timezone.now())
        Activity.objects.create(user=users[2], type='Detective Work', duration=90, date=timezone.now())
        Activity.objects.create(user=users[3], type='Flight', duration=30, date=timezone.now())

        # Create Workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength training for superheroes')
        w2 = Workout.objects.create(name='Agility Drills', description='Agility and speed drills')
        w1.suggested_for.set([marvel, dc])
        w2.suggested_for.set([marvel])

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)


        # Ensure unique index on email using pymongo
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client[settings.DATABASES['default']['NAME']]
        db.user.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
