from django.core.management.base import BaseCommand
from testform.scripts.elastic import insert_all

class Command(BaseCommand):
    def handle(self, *args, **options):
        insert_all()