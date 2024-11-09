from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Create default super user and token'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str)
        parser.add_argument('--password', type=str)
        parser.add_argument('--email', type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        password = options['password']
        email = options['email']
        if not User.objects.filter(username=username).exists():
            new_user = User.objects.create_superuser(username, email, password)
            Token.objects.create(user=new_user)
