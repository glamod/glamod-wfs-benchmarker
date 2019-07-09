import logging
import random

from locust import HttpLocust, TaskSet, task


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class UserTasks(TaskSet):

#    def wait_function(self):
#        return 10 #waiter()

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass #log.warn('STOP')

    def _year(self):
        return random.randint(1861, 2010)

    def _month(self):
        return random.randint(1, 8)

    def _var_code(self, n=1):
        if n == 1: return 85
        sample = random.sample([36, 41, 85, 86, 89, 93, 94, 44, 47, 50, 33, 38, 40, 57, 58, 
                                104, 105, 107, 108, 109], k=(n - 1))
        sample.append(85)
        return '(' + ','.join([str(_) for _ in sample]) + ')'

    def _bbox(self):
        return '-50,-50,50,50'

    @task(1)
    def capabilities(self):
        query = '/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetCapabilities'

        with self.client.get(query, catch_response=True, name='capabilities') as response:
            if b'<ows:IndividualName>William Tucker</ows:IndividualName>' not in response.content:
                resopnse.failure('Capabilities does not match expected XML')

        self.client.get(query, name='capabilities')

    @task(1)
    def station_ids(self):
        record_count = random.randint(500, 100000) 
        query = '/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetFeature&typename=station_configuration&outputFormat=json&propertyName=primary_id&count={}'.format(record_count)
        self.client.get(query, name='station_ids')

    @task(1)
    def query_bbox_time(self):
        start_year = self._year()
        end_year = start_year + random.randint(0, 5)
        start_month = self._month()
        end_month = start_month + 4
        var_codes = self._var_code(2)
        bbox = self._bbox()

        query = '/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetFeature&typename=observations_table&outputFormat=json&cql_filter=date_time%20DURING%20{}-{:02d}-01T00:00:00Z/{}-{:02d}-28T00:00:00Z%20AND%20report_type=2%20AND%20observed_variable%20IN%20{}%20AND%20BBOX(location,{})'.format(start_year, start_month, end_year, end_month, var_codes, bbox)

        with self.client.get(query, name='query_bbox_time', catch_response=True) as response:
            json = response.json()
            assert('totalFeatures' in json)

        log.info('Query: {}'.format(query))

    @task(2)
    def table_counts(self):
        var_code = self._var_code()
        year = self._year()
        report_type = random.choice([0, 2, 3])

        self.client.get('/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetFeature&typename=observation_counts&outputFormat=json&cql_filter=year={}%20AND%20var_code={}%20AND%20report_type={}'.format(year, var_code, report_type), name='table_counts')


class WebsiteUser(HttpLocust):

    task_set = UserTasks
    min_wait = 100
    max_wait = 2000
    host = 'http://glamod1.ceda.ac.uk'





