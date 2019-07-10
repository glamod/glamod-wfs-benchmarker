"""
deterministic_tasks
===================

Generators for deterministic tasks that we can compare directly.

"""

# Bboxes are w,s,e,n
_BBOXES = [
'-180,-90,0,0',
'0,-90,180,0',
'0,0,180,90',
'-180,0,0,90'
]

_REPORT_TYPES = [0, 2, 3]
 

class _BaseQueryGenerator(object):

    counter = 0

    def __init__(self):
        self._queries = []
        self._create_queries()


    def _create_queries(self):
        raise NotImplementedError()

   
    def get_next(self):
        count = self.__class__.counter
    
        if count >= len(self._queries):
            return None
 
        query = self._queries[count]
        self.__class__.counter += 1        
        return query


class TimeBBoxQueryGenerator(_BaseQueryGenerator):

    def _create_queries(self):

        for year in range(1950, 2011):
            for start_month in range(1, 7):

                for bbox in _BBOXES: 
                    for report_type in _REPORT_TYPES:
                        if report_type == 0 and year < 1980: continue

                        if report_type == 0:
                            end_month = start_month
                        else:
                            end_month = start_month + 6

                        query = '/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetFeature&typename=observations_table&outputFormat=json&cql_filter=date_time%20DURING%20{}-{:02d}-01T00:00:00Z/{}-{:02d}-28T00:00:00Z%20AND%20report_type={}%20AND%20BBOX(location,{})'.format(year, start_month, year, end_month, report_type, bbox)
                        self._queries.append(query) 


class StationIDQueryGenerator(_BaseQueryGenerator):

    def _create_queries(self):
        for record_count in range(500, 1000000, 100):
            query = '/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetFeature&typename=station_configuration&outputFormat=csv&propertyName=primary_id&count={}'.format(record_count)
            self._queries.append(query)


class StationTimeSeriesGenerator(_BaseQueryGenerator):

    def _create_queries(self):

        for start_year in range(1869, 1970):
            end_year = start_year + 40

            query = '/geoserver/glamod/ows?service=WFS&version=2.0.0&request=GetFeature&typename=observations_table&outputFormat=json&cql_filter=report_id%20ILIKE%20%27AGE00135%25%27%20AND%20date_time%20DURING%20{}-01-01T00:00:00Z/{}-12-31T23:59:59Z%20AND%20observed_variable%20IN%20(44,85)'.format(start_year, end_year)
            self._queries.append(query)


query_generators = {}
query_generators['time_bbox'] = TimeBBoxQueryGenerator()
query_generators['station_ids'] = StationIDQueryGenerator()
query_generators['station_time_series'] = StationTimeSeriesGenerator()
