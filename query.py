#

from uuid import uuid4
from random import randint
from os import getenv

from flask import Flask
from flask_restful import Resource, Api, reqparse

import re


# Concrete API's should extend abstract RESTful "Resource" class 
# From this class expose methods for each supported HTTP method.
class query_range_api(Resource):
    '''
    "/query_range" mock API for swatch-metrics (Metering) scale testing.
    '''
    def timeseries_data(self, suffix_id, product_name, start_time) -> dict:
        # Returns timeseries data
        return {
                    "metric": {
                        "_id": uuid4().__str__(),
                        "billing_marketplace_account": f"mktp-{suffix_id}",
                        "billing_model": "marketplace",
                        "billing_provider": "aws",
                        "ebs_account": f"account{suffix_id}",
                        "external_organization": f"org{suffix_id}",
                        "product": f"{product_name}",
                        "support": "Premium"
                    },
                    "values": [
                                [
                                    f"{start_time}",
                                    randint(1, 100)
                                ]
                        ]
                }

    def get(self, ) -> dict:
        # RequestParser to capture query_parameters from a request
        #parser = reqparse.RequestParser()

        # add an argument to be parsed
        # /api/v1/query_range?query=kafka_id%3Akafka_broker_quota_totalstorageusedbytes%3Amax_over_time1h_gibibyte_months%20*%20on%28_id%29%20group_right%20min_over_time%28subscription_labels%7Bproduct%3D%22rhosak%22%2C%20external_organization%3D%22org123%22%2C%20billing_model%3D%22marketplace%22%2C%20support%3D~%22Premium%7CStandard%7CSelf-Support%7CNone%22%7D%5B1h%5D%29&start=1687150800&end=1687320000&step=3600&timeout=10000
        #parser.add_argument('query')
        #parser.add_argument('start')

        # parse all arguments from the provided request
        #args = parser.parse_args()
        
        # capture product and org_id infromation from the Request query
        #product_label = re.sub(r'.*product=\"(.*)\", external.+', r'\1', args['query'])
        #org_id_suffix = re.sub(r'.*org([0-9]+).*', r'\1', args['query'])
        
        # Generate timeseries data
        SYSTEM_PER_ORGANIZATION = getenv('SYS_PER_ORG', '10')
        return {
            'status': 'success',
            'data': {
                'resultType': 'matrix',
                'result': [
                    self.timeseries_data('123', 'rhosak', 1687150800) for item in range(10)
                ]
            }
        }


if __name__ == '__main__':

    # create a Flask app and main entrypoint for the application
    app = Flask(__name__)
    api = Api(app)

    # adds a resource to the api.
    api.add_resource(query_range_api, '/api/v1/query_range')

    # run the application on a local development server
    # PROM_URL = http://swatch-prometheus-service.rhsm-perf.svc.cluster.local:9090/api/v1/
    app.run(port=8091)# (port=8090)
