import pytest
import mock
import logging
import datetime
from dateutil.tz import tzlocal
from get_k8s_pod_suffix import get_pod_suffix

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


class DictAttributes:
    # Create attributes from dictonary to mimic k8s api
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, list):
                setattr(self, a, [DictAttributes(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, DictAttributes(b) if isinstance(b, dict) else b)

    def get(self, app, success=True):
        if success:
            return "pgbouncer"
        else:
            return "something_wrong"

    def strftime(self, fmt):
        pass


class MockK8sApi:
    def __init__(self, pods=None, rs=None):
        self.pods = pods
        self.rs = rs

    def list_namespaced_pod(self, namespace=None):
        return DictAttributes(self.pods)

    def read_namespaced_replica_set_status(self, name=None, namespace=None):
        if isinstance(self.rs, list):
            for replicaset in self.rs:
                if replicaset['metadata']['name'] == name:
                    return DictAttributes(replicaset)
        return None


# Tests
@mock.patch('get_k8s_pod_suffix.k8s_client_config')
def test_suffix_is_not_set_for_one_pod(mocked_config):
    mocked_config.return_value = (MockK8sApi(pods=one_pod), MockK8sApi(rs=one_pod))
    suffix = get_pod_suffix(pod_name="pgbouncer", pod_namespace="test", logger=logging.getLogger('rds-cleaner'))
    assert suffix is None


@mock.patch('get_k8s_pod_suffix.k8s_client_config')
def test_suffix_is_set_for_first_pod(mocked_config):
    mocked_config.return_value = (
        MockK8sApi(pods=two_pods_one_rs), MockK8sApi(rs=one_rs))
    suffix = get_pod_suffix(pod_name="pgbouncer-1", pod_namespace="test-ordering-pods",
                            logger=logging.getLogger('rds-cleaner'))
    assert suffix == "-1"


@mock.patch('get_k8s_pod_suffix.k8s_client_config')
def test_suffix_is_set_for_second_pod(mocked_config):
    mocked_config.return_value = (
        MockK8sApi(pods=two_pods_one_rs), MockK8sApi(rs=one_rs))
    suffix = get_pod_suffix(pod_name="pgbouncer-2", pod_namespace="test-ordering-pods",
                            logger=logging.getLogger('rds-cleaner'))
    assert suffix == "-2"


@mock.patch('get_k8s_pod_suffix.k8s_client_config')
def test_suffix_is_set_for_new_first_pod_during_rolling_update(mocked_config):
    mocked_config.return_value = (
        MockK8sApi(pods=four_pods_in_two_rs), MockK8sApi(rs=two_rs))
    suffix = get_pod_suffix(pod_name="pgbouncer-new-1", pod_namespace="test-ordering-pods",
                            logger=logging.getLogger('rds-cleaner'))
    assert suffix == "-1"


@mock.patch('get_k8s_pod_suffix.k8s_client_config')
def test_suffix_is_set_for_second_first_pod_during_rolling_update(mocked_config):
    mocked_config.return_value = (MockK8sApi(pods=four_pods_in_two_rs),
                                  MockK8sApi(rs=two_rs))
    suffix = get_pod_suffix(pod_name="pgbouncer-new-2", pod_namespace="test-ordering-pods",
                            logger=logging.getLogger('rds-cleaner'))
    assert suffix == "-2"


@mock.patch('get_k8s_pod_suffix.k8s_client_config')
def test_fail_when_pod_doesnt_exist(mocked_config):
    mocked_config.return_value = (MockK8sApi(pods=four_pods_in_two_rs),
                                  MockK8sApi(rs=two_rs))
    with pytest.raises(KeyError, match='pgbouncer-new-3'):
        get_pod_suffix(pod_name="pgbouncer-new-3", pod_namespace="test-ordering-pods",
                       logger=logging.getLogger('rds-cleaner'))
