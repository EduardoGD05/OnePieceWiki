import requests
from django.core.management.base import BaseCommand
from WikiPage.models import Saga, Arc, Chapter

class Command(BaseCommand):
    help = 'Importa los capítulos desde la API de One Piece'

    def handle(self, *args, **options):
        try:
            # URL de la API para los capítulos
            chapter_url = 'https://api.api-onepiece.com/v2/episodes/en'
            response = requests.get(chapter_url)
            response.raise_for_status()
            chapter_data = response.json()

            # Importar los capítulos
            for chapter in chapter_data:
                # Obtener la saga asociada
                saga_id = chapter.get('saga', {}).get('id') 
                if saga_id:
                    try:
                        saga_obj = Saga.objects.get(id=saga_id)
                    except Saga.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Saga con ID {saga_id} no encontrada para el capítulo "{chapter["title"]}"'))
                        continue 

                    # Obtener o crear el arco (arc) asociado
                    arc_obj, created = Arc.objects.get_or_create(
                        title=chapter['arc']['title'],
                        defaults={'description': chapter['arc']['description']}
                    )

                    # Crear o actualizar el capítulo
                    chapter_obj, created = Chapter.objects.get_or_create(
                        number=chapter['number'],
                        title=chapter['title'],
                        defaults={
                            'description': chapter['description'],
                            'chapter': chapter['chapter'],
                            'release_date': chapter['release_date'],
                            'saga': saga_obj,
                            'arc': arc_obj
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Capítulo "{chapter_obj.title}" importado correctamente'))
                    else:
                        self.stdout.write(self.style.WARNING(f'El capítulo "{chapter_obj.title}" ya existe'))

                else:
                    self.stdout.write(self.style.WARNING(f'No se encontró la saga para el capítulo "{chapter["title"]}"'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error al obtener los datos de los capítulos: {e}'))