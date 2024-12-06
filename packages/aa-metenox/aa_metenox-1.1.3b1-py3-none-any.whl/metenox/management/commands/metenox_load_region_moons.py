from django.core.management import BaseCommand

from metenox import tasks


class Command(BaseCommand):
    help = "Loads all non highsec moons in a region with a 0 value to see which moons are missing a scan"

    def add_arguments(self, parser):
        parser.add_argument("region_id", type=int)

    def handle(self, *args, **kwargs):
        region_id = kwargs["region_id"]
        tasks.load_region_moons.delay(region_id)
