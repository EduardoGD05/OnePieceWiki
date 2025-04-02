from WikiPage.models import Character, Crew, Fruit
import requests
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Importa personajes desde la API oficial de One Piece'

    def handle(self, *args, **options):
        try:
            response = requests.get('https://api.api-onepiece.com/v2/characters/en')  
            response.raise_for_status()
            characters_data = response.json()

            for character in characters_data:
                # Datos del personaje
                character_name = character.get('name')
                character_birthday = character.get('birthday', 'Desconocido')
                character_age = character.get('age', 'Desconocido')
                character_bounty = character.get('bounty', 'Desconocido')
                
                character_status = character.get('status', '')
                if not character_status:
                    character_status = 'Desconocido'

                # Obtener y crear el Crew (tripulación)
                crew_data = character.get('crew', {})
                crew_name = crew_data.get('name', 'Desconocido')
                crew_description = crew_data.get('description', 'Sin descripción')
                crew_number = crew_data.get('number', 'Desconocido')
                
                # Validar si 'crew_number' es un número válido. Si no lo es, asignamos un valor predeterminado (0 o -1).
                try:
                    crew_number = int(crew_number)  # Intentamos convertirlo a entero
                except ValueError:
                    crew_number = 0  

                # Extraer el valor de 'is_yonko', si está disponible, o asignar False por defecto
                is_yonko = crew_data.get('is_yonko', False)

                crew, created = Crew.objects.get_or_create(
                    name=crew_name,
                    defaults={
                        'description': crew_description,
                        'number': crew_number,  # Asignamos el valor de 'crew_number'
                        'is_yonko': is_yonko  # Asignar el valor de 'is_yonko'
                    }
                )

                # Obtener y crear el Fruit (fruto)
                fruit_data = character.get('fruit', {})
                fruit_name = fruit_data.get('name', 'Desconocido').strip()
                if not fruit_name:  # Si es vacío o nulo, asigna un nombre por defecto
                    fruit_name = 'Desconocido'

                fruit, created = Fruit.objects.get_or_create(
                    name=fruit_name,
                    defaults={
                        'description': fruit_data.get('description', 'Sin descripción'),
                        'type': fruit_data.get('type', 'Desconocido'),
                        'filename': fruit_data.get('filename', ''),
                        'roman_name': fruit_data.get('roman_name', 'Desconocido'),
                        'technicalFile': fruit_data.get('technicalFile', '')
                    }
                )

                # Crear o actualizar el personaje
                character_obj, created = Character.objects.get_or_create(
                    name=character_name,
                    defaults={
                        'birthday': character_birthday,
                        'age': character_age,
                        'bounty': character_bounty,
                        'status': character_status,
                        'crew': crew,
                        'fruit': fruit
                    }
                )

                self.stdout.write(self.style.SUCCESS(f'Personaje "{character_name}" importado correctamente'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error al obtener los personajes desde la API: {e}'))