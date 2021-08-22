import _io
import abc
import logging
from collections import deque

from elasticsearch.helpers import parallel_bulk, bulk

import injector.config


class Injectable(abc.ABC):
    def __init__(self, config: injector.config.Config,
                 raw_data: object = None,
                 data_file: _io.TextIOWrapper = None,
                 data_file_path: str = None):
        self.config: injector.config.Config = config
        self.data_file: _io.TextIOWrapper = data_file
        self.logger = logging.getLogger(self.__class__.__name__)
        self.data_file_path: str = data_file_path
        self.raw_data: object = raw_data

    def before_inject(self):
        if self.config.elastic_index_mapping_file:
            self.logger.info(f"Trying to create {self.config.elastic_index} index...")
            self.config.elastic_search.indices.create(index=self.config.elastic_index, ignore=400,
                                                      body=self.config.elastic_index_mapping_file.read())

    @abc.abstractmethod
    def inject_impl(self):
        pass

    def inject(self):
        self.before_inject()
        self.inject_impl()

    def bulk_inserts(self, actions: list):
        if len(actions) >= 100:
            deque(parallel_bulk(self.config.elastic_search, actions), maxlen=0)
        else:
            bulk(self.config.elastic_search, actions)
