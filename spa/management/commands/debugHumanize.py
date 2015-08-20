import humanize
from django.core.management.base import NoArgsCommand
from spa.models.activity import Activity


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            activity = Activity.objects.get(pk=13437)
            if activity is not None:
                date = humanize.naturaltime(activity.date.replace(tzinfo=None))
                print(date)
        except Exception as ex:
            print("Debug exception: %s" % ex.message)