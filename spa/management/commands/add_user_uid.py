import uuid

from django.core.management.base import NoArgsCommand

from spa.models import UserProfile


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            users = UserProfile.objects.exclude(uid__isnull=False)
            for user in users:
                user.uid = uuid.uuid4()
                user.save()
        except Exception as ex:
            print("Debug exception: %s" % ex)