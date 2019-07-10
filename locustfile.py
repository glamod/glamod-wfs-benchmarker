import logging
import random

from locust import HttpLocust, TaskSet, task

from deterministic_tasks import query_generators

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

HOST = 'http://glamod1.ceda.ac.uk'


class UserTasks(TaskSet):

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass


    def _year(self):
        return random.randint(1861, 2010)


    def _var_code(self, n=1):
        if n == 1: return 85
        sample = random.sample([36, 41, 85, 86, 89, 93, 94, 44, 47, 50, 33, 38, 40, 57, 58, 
                                104, 105, 107, 108, 109], k=(n - 1))
        sample.append(85)
        return '(' + ','.join([str(_) for _ in sample]) + ')'


    @task(1)
    def get_capabilities(self):
        query = '/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetCapabilities'

        with self.client.get(query, catch_response=True, name='capabilities') as response:
            if b'<ows:IndividualName>William Tucker</ows:IndividualName>' not in response.content:
                resopnse.failure('Capabilities does not match expected XML')

        self.client.get(query, name='capabilities')

    @task(3)
    def query_station_ids(self):
        name = 'station_ids'
        query = query_generators[name].get_next()
        record_count = int(query.split('=')[-1])
        
        with self.client.get(query, name=name, catch_response=True) as response:
            n_lines = len(response.text.split('\n'))
            assert(record_count == (n_lines - 2))

        log.debug('Query: {}{}'.format(HOST, query))


    @task(3)
    def query_time_bbox(self):
        name = 'time_bbox'
        query = query_generators[name].get_next()

        with self.client.get(query, name=name, catch_response=True) as response:
            json = response.json()
            assert('totalFeatures' in json)

        log.debug('Query: {}{}'.format(HOST, query))


    @task(3)
    def station_time_series(self):
        name = 'station_time_series'
        query = query_generators[name].get_next()

        with self.client.get(query, name=name, catch_response=True) as response:
            json = response.json()
            assert('totalFeatures' in json)
            assert(json['totalFeatures'] > 10)

        log.debug('Query: {}{}'.format(HOST, query))


    @task(2)
    def query_table_counts(self):
        var_code = self._var_code()
        year = self._year()
        report_type = random.choice([0, 2, 3])

        self.client.get('/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetFeature&typename=observation_counts&outputFormat=json&cql_filter=year={}%20AND%20var_code={}%20AND%20report_type={}'.format(year, var_code, report_type), name='table_counts')


class WebsiteUser(HttpLocust):

    task_set = UserTasks
    min_wait = 100
    max_wait = 2000
    host = HOST






