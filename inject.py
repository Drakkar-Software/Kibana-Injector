import argparse
import logging

import injector.config
import injector.inject_factory as inject_factory


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Inject OctoBot metrics to kibana.')
    parser.add_argument("--mongo-file", help="the exported mongo file", type=argparse.FileType('r'))
    parser.add_argument("--elastic-index", help="the elastic index name", type=str)
    parser.add_argument("--elastic-host", help="the elastic index name", type=str)
    parser.add_argument("--elastic-api-key", help="the elastic api key", type=str)
    parser.add_argument("--elastic-api-secret", help="the elastic api secret", type=str)
    parser.add_argument("--elastic-index-mapping-file", help="the elastic index mapping file",
                        type=argparse.FileType('r'))
    parser.add_argument("--elastic-timestamp-field-name", help="the elastic api secret", type=str)
    args = parser.parse_args()

    config = injector.config.Config(elastic_index=args.elastic_index,
                                    elastic_host=args.elastic_host,
                                    elastic_api_key=args.elastic_api_key,
                                    elastic_api_secret=args.elastic_api_secret,
                                    elastic_index_mapping_file=args.elastic_index_mapping_file,
                                    elastic_timestamp_field_name=args.elastic_timestamp_field_name)
    injectable_instance = inject_factory.create_injectable_instance(config, args)
    injectable_instance.inject()


if __name__ == '__main__':
    main()
