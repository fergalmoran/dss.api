from datetime import datetime
from django.test import TestCase
from spa.models import Show
from spa.models.show import ShowOverlapException

DATE_FORMAT = '%d/%m/%Y %H:%M:%S'
START_DATE = datetime.strptime("28/04/2013 12:00:00", DATE_FORMAT)
END_DATE = datetime.strptime("28/04/2013 13:00:00", DATE_FORMAT)


class TestScheduleOverlaps(TestCase):
    def setUp(self):
        Show.objects.all().delete()
        Show(description="Test event one", start=START_DATE, end=END_DATE).save()

    def test_first_show_saved(self):
        self.assertEqual(len(Show.objects.all()), 1)

    def test_same_event_overlap(self):
        try:
            Show(description="Test overlapping event", start=START_DATE, end=END_DATE).save()
            self.fail("Shows cannot overlap each other")
        except ShowOverlapException:
            pass
        except Exception, ex:
            self.fail(ex.message)

    def test_two_events_flush(self):
        try:
            start = datetime.strptime("28/04/2013 13:00:00", DATE_FORMAT)
            end = datetime.strptime("28/04/2013 14:00:00", DATE_FORMAT)
            Show(description="Another show begins in middle of this show", start=start, end=end).save()
        except ShowOverlapException:
            self.fail("These events do not overlap, they are flush")
        except Exception, ex:
            self.fail(ex.message)

    def test_event_straddle_start_end(self):
        try:
            start = datetime.strptime("28/04/2013 11:30:00", DATE_FORMAT)
            end = datetime.strptime("28/04/2013 12:30:00", DATE_FORMAT)
            Show(description="Another show begins in middle of this show", start=start, end=end).save()
            self.fail("Should not be able to save a show straddling another show")
        except ShowOverlapException:
            pass
        except Exception, ex:
            self.fail(ex.message)

    def test_event_straddle_end_start(self):
        try:
            start = datetime.strptime("28/04/2013 12:30:00", DATE_FORMAT)
            end = datetime.strptime("28/04/2013 13:30:00", DATE_FORMAT)
            s = Show(description="Show begins in middle of another show", start=start, end=end)
            s.save()
            import ipdb; ipdb.set_trace()
            self.fail("Should not be able to save a show straddling another show")
        except ShowOverlapException:
            pass
        except Exception, ex:
            self.fail(ex.message)
