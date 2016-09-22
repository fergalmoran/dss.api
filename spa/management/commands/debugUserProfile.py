from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            users = User.objects.all()
            for user in users:
                try:
                    if user.get_profile() is None:
                        print("Invalid user: %s" % user.username)
                except:
                    print("Invalid user: %s" % user.username)
                    user.save()

            pass
        except Exception as ex:
            print("Debug exception: %s" % ex.message)