import requests
from django.core.management.base import BaseCommand
from WikiPage.models import Saga

class Command(BaseCommand):
    help = 'Importa las sagas desde la API de One Piece'

    def handle(self, *args, **options):
        try:
            # URL de la API para las sagas
            saga_url = 'https://api.api-onepiece.com/v2/sagas/en'  # Cambia esta URL si es diferente
            response = requests.get(saga_url)
            response.raise_for_status()
            saga_data = response.json()

            # Importar las sagas
            for saga in saga_data:
                saga_obj, created = Saga.objects.get_or_create(
                    title=saga['title'],
                    defaults={
                        'saga_number': saga['saga_number'],
                        'saga_chapitre': saga['saga_chapitre'],
                        'saga_volume': saga['saga_volume'],
                        'saga_episode': saga['saga_episode'],
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Saga "{saga_obj.title}" importada correctamente'))
                else:
                    self.stdout.write(self.style.WARNING(f'La saga "{saga_obj.title}" ya existe'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error al obtener los datos de las sagas: {e}'))