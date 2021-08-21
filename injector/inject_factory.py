import injector.config
import injector.injectable.injectable as injectable
import injector.injectable.exported_mongo_file as mongo


def create_injectable_instance(config: injector.config.Config, args) -> injectable.Injectable:
    if args.mongo_file:
        return mongo.ExportedMongoFile(config=config, data_file=args.mongo_file)
