import random
from django.core.management.base import NoArgsCommand
from spa.models.comment import Comment


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            comments = Comment.objects.all()
            for comment in comments:
                mix = comment.mix
                time_index = random.randrange(50, comment.mix.duration)
                comment.time_index = time_index

                comment.save()
                print("Timeindex: %d Mix: %s Comment: %s" % (time_index, comment.mix.slug, comment.comment))
        except Exception as ex:
            print("Debug exception: %s" % ex.message)