import datetime
from dateutil.tz import tzlocal

# pod details k8s api calls
one_pod = {'items': [{'metadata': {
    'labels': {u'app': 'pgbouncer'},
    'name': 'pgbouncer',
    'owner_references': [{'name': 'pgbouncer-rs'}],
    'creation_timestamp': datetime.datetime(2019, 3, 26, 15, 55, 2, tzinfo=tzlocal())}}]}

two_pods_one_rs = {'items': [{'metadata': {
    'labels': {u'app': 'pgbouncer'},
    'name': 'pgbouncer-1',
    'owner_references': [{'name': 'pgbouncer-rs'}],
    'creation_timestamp': datetime.datetime(2019, 3, 26, 15, 55, 2, tzinfo=tzlocal())}},
    {'metadata': {
        'labels': {u'app': 'pgbouncer'},
        'name': 'pgbouncer-2',
        'owner_references': [{'name': 'pgbouncer-rs'}],
        'creation_timestamp': datetime.datetime(2019, 3, 26, 15, 55, 2, tzinfo=tzlocal())}}]}

four_pods_in_two_rs = {'items': [{'metadata': {
    'labels': {u'app': 'pgbouncer'},
    'name': 'pgbouncer-old-1',
    'owner_references': [{'name': 'pgbouncer-rs-old'}],
    'creation_timestamp': datetime.datetime(2019, 3, 26, 15, 55, 2, tzinfo=tzlocal())}},
    {'metadata': {
        'labels': {u'app': 'pgbouncer'},
        'name': 'pgbouncer-old-2',
        'owner_references': [{'name': 'pgbouncer-rs-old'}],
        'creation_timestamp': datetime.datetime(2019, 3, 26, 15, 55, 2, tzinfo=tzlocal())}},
    {'metadata': {
        'labels': {u'app': 'pgbouncer'},
        'name': 'pgbouncer-new-1',
        'owner_references': [{'name': 'pgbouncer-rs-new'}],
        'creation_timestamp': datetime.datetime(2019, 3, 27, 0, 0, 0, tzinfo=tzlocal())}},
    {'metadata': {
        'labels': {u'app': 'pgbouncer'},
        'name': 'pgbouncer-new-2',
        'owner_references': [{'name': 'pgbouncer-rs-new'}],
        'creation_timestamp': datetime.datetime(2019, 3, 27, 0, 0, 0, tzinfo=tzlocal())}}]}

# replica sets api call response
one_rs = {'metadata': {'creation_timestamp': datetime.datetime(2019, 3, 29, 16, 0, 30, tzinfo=tzlocal()),
                       'labels': {u'app': 'pgbouncer'},
                       'name': 'pgbouncer-rs',
                       'namespace': 'test-ordering-pods',
                       'owner_references': [{'name': 'pgbouncer'}]}}

two_rs = [{'metadata': {'creation_timestamp': datetime.datetime(2019, 3, 27, 0, 0, 0, tzinfo=tzlocal()),
                        'labels': {u'app': 'pgbouncer'},
                        'name': 'pgbouncer-rs-new',
                        'namespace': 'test-ordering-pods',
                        'owner_references': [{'name': 'pgbouncer'}]}},
          {'metadata': {'creation_timestamp': datetime.datetime(2019, 3, 26, 0, 0, 0, tzinfo=tzlocal()),
                        'labels': {u'app': 'pgbouncer'},
                        'name': 'pgbouncer-rs-old',
                        'namespace': 'test-ordering-pods',
                        'owner_references': [{'name': 'pgbouncer'}]}}]

