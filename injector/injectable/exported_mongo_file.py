import json
import datetime
import pandas as pd
import injector.injectable.injectable as injectable


class ExportedMongoFile(injectable.Injectable):
    def inject_impl(self):
        self.logger.info(f"Loading mongo file...")
        data = pd.read_json(self.data_file.read(), lines=True)
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
            key: data[key] if key != "startedAt" else self.convert_time(data[key])
            for key in data.keys()
        }

    @staticmethod
    def convert_time(timestamp) -> str:
        return datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y %H:%M:%S')
