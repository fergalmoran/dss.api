from allauth.socialaccount.models import SocialAccount
from django.core.files.base import ContentFile
from django.core.management.base import NoArgsCommand
from requests import request, ConnectionError
from spa.models.userprofile import UserProfile


def save_image(profile, url):
    try:
        response = request('GET', url)
        response.raise_for_status()
    except ConnectionError:
        pass
    else:
        profile.avatar_image.save(u'',
                                  ContentFile(response.content),
                                  save=False)
        profile.save()


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            for user in UserProfile.objects.all():
                try:
                    print "Getting image for {0}".format(user.slug)
                    social_account = SocialAccount.objects.get(user=user.user)
                    if social_account:
                        try:
                            provider_account = social_account.get_provider_account()
                            if provider_account:
                                avatar_url = provider_account.get_avatar_url()
                                save_image(user, avatar_url)
                        except Exception, ex:
                            print ex.message
                    else:
                        print "No account for {0}".format(user.slug)

                except SocialAccount.DoesNotExist:
                    pass
                except Exception, ex:
                    print "Debug exception: %s" % ex.message
        except Exception, ex:
            print "Debug exception: %s" % ex.message
