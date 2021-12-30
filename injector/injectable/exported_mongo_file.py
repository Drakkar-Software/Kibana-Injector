import json
import datetime
from io import StringIO

import pandas as pd
import injector.injectable.injectable as injectable


class ExportedMongoFile(injectable.Injectable):
    def inject_impl(self):
        self.logger.info("Loading mongo file...")
        try:
            data = pd.read_json(StringIO(self.data_file.read()), lines=True)  # https://stackoverflow.com/questions/63553845/pandas-read-json-valueerror-protocol-not-known
        except ValueError:
            self.logger.error("Error when loading json file.")
            return
        actions = [
            {
                "_index": self.config.elastic_index,
                "_id": raw[0]['$oid'],
                "_source": json.dumps(self.convert(raw[1]))
             }
            for raw in data.values
        ]
        self.logger.info(f"Inserting mongo data...")
        self.bulk_inserts(actions)

    def convert(self, data) -> dict:
        return {
            key: data[key] if key not in self.config.elastic_timestamp_field_names else self.convert_time(data[key])
            for key in data.keys()
        }

    @staticmethod
    def convert_time(timestamp) -> str:
        return datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
