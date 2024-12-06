from datetime import datetime
from zoneinfo import ZoneInfo
from django.utils import timezone
from tests.__init__ import *
from psplpy.django_utils import *


def tests():
    db = Database(engine=Database.POSTGRESQL, name=get_env('DB_USER'), host=get_env('DB_HOST'), port=get_env('DB_PORT'),
                  user=get_env('DB_USER'), password=get_env('DB_PW'), TIME_ZONE='UTC')
    assert timezone.get_current_timezone() == ZoneInfo('UTC')

    class Test(db.Model):
        name = models.CharField(max_length=200, null=True)
        email = models.EmailField(null=True)
        time = models.DateTimeField(default=timezone.now())

    Test.init()

    naive_time = datetime(2020, 1, 1, 0, 0)
    aware_time = timezone.make_aware(naive_time)
    print(naive_time, aware_time)

    test = Test(name='me', email='test@test.com', time=aware_time)
    test.save()

    all_values = [list(item.values()) for item in Test.objects.all().values()]
    print(all_values)
    assert all_values[0] == [1, 'me', 'test@test.com', aware_time]


if __name__ == '__main__':
    tests()
