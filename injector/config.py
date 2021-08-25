import os
from elasticsearch import Elasticsearch


class Config:
    def __init__(self, elastic_host=None, elastic_index=None,
                 elastic_api_key=None, elastic_api_secret=None, elastic_index_mapping_file=None,
                 elastic_timestamp_field_names=["timestamp"]):
        self.elastic_host = elastic_host
        self.elastic_index = elastic_index
        self.elastic_api_key = elastic_api_key
        self.elastic_api_secret = elastic_api_secret
        self.elastic_index_mapping_file = elastic_index_mapping_file
        self.elastic_timestamp_field_names = elastic_timestamp_field_names
        self.elastic_search = None
        self._load_env()
        self._initialize()

    def _initialize(self):
        self._validate()
        self.elastic_search = Elasticsearch(hosts=[self.elastic_host],
                                            api_key=(self.elastic_api_key, self.elastic_api_secret))

    def _load_env(self):
        if not self.elastic_host:
            self.elastic_host = os.environ.get('ELASTICSEARCH_URI', None)
        if not self.elastic_index:
            self.elastic_index = os.environ.get('ELASTICSEARCH_INDEX', None)
        if not self.elastic_api_key:
            self.elastic_api_key = os.environ.get('ELASTICSEARCH_API_KEY', None)
        if not self.elastic_api_secret:
            self.elastic_api_secret = os.environ.get('ELASTICSEARCH_API_SECRET', None)

    def _validate(self):
        if not self.elastic_host or not self.elastic_index \
                or not self.elastic_api_key or not self.elastic_api_secret:
            raise Exception("Error: missing mandatory elastic configuration")
