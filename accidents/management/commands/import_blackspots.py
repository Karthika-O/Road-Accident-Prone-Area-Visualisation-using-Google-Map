import csv
from django.core.management.base import BaseCommand
from accidents.models import Accident  # Replace 'accidents' with your actual app name if different

class Command(BaseCommand):
    help = 'Import accident blackspot data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        count = 0

        def extract_lat_lng(coord_str):
            try:
                lat, lng = coord_str.strip().split(',')
                return float(lat), float(lng)
            except:
                return None, None

        with open(csv_path, encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)
            for row in reader:
                lat, lng = extract_lat_lng(row['GEOGRAPHICAL COORDINATES (STARTING POINT (LAT,LONG))'])
                if lat is not None and lng is not None:
                    Accident.objects.create(
                        district=row['Name of District'],
                        police_station=row['Name of Police Station'],
                        location=row['Location of Accident Spot'],
                        road_name=row['Name of Road'],
                        latitude=lat,
                        longitude=lng,
                        total_accidents=int(row['Total accidents (Fatal+Grievous)']),
                        total_fatalities=int(row['Total Fatalities']),
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully imported {count} accident records"))
