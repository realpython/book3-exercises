from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from optparse import make_option
from bson.json_util import loads
from pymongo import MongoClient
from os.path import splitext


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--collection', '-c',
                    dest='collection',
                    help='MongoDB collection where the data will be loaded.'),
    )

    help = "Loads data from files into the MongoDB database.\n\n" \
           "Usage: manage.py mongo_load FILE"

    def handle(self, *args, **options):
        if not args:
            raise CommandError('No data filename provided.')

        collection = options.get('collection')

        connection = MongoClient()
        db = connection[settings.MONGODB_NAME]

        if not collection:
            name = splitext(args[0])[0]
            items = db[name]
        else:
            items = db[collection]

        with open(args[0], 'r') as f:
            for line in f:
                items.insert(loads(line))
