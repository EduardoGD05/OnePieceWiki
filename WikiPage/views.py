from django.shortcuts import render, get_object_or_404  
from .models import Crew, Fruit, Character, Saga, Arc, Chapter
from django.db.models import Q
import re
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator

def home(request):
<<<<<<< HEAD
    return render(request,'WikiPage/onepiece.html',{'page_title': ''})
 
=======
    return render(request,'WikiPage/onepiece.html',{'page_title': 'CATEGORÍAS'})

>>>>>>> 8db554aa88061167e621b44a16477069e9491d13
def crew_list(request):
    crews = Crew.objects.all()
    paginator = Paginator(crews, 10)  
    page_number = request.GET.get('page') 
    page_crews = paginator.get_page(page_number) 
    return render(request,'WikiPage/crews.html',{'page_title':'TRIPULACIONES DE ONE PIECE', 'crews':page_crews})

def fruits_list(request):
    fruits =Fruit.objects.all()
    paginator = Paginator(fruits, 10)  
    page_number = request.GET.get('page') 
    page_fruits = paginator.get_page(page_number) 
    return render(request,'WikiPage/fruits.html',{'page_title':'FRUTAS DEL DIABLO', 'fruits':page_fruits})
    
def character_list(request):
    characters = Character.objects.all()
    paginator = Paginator(characters, 10)  
    page_number = request.GET.get('page') 
    page_characters = paginator.get_page(page_number) 
    return render(request,'WikiPage/characters.html',{'page_title':'PERSONAJES', 'characters':page_characters})
    
def saga_list (request):
    sagas = Saga.objects.all()
    return render(request, 'WikiPage/sagas.html', {'page_title':'SAGAS DE ONE PIECE', 'sagas':sagas})
    
def arc_list(request):
    arcs = Arc.objects.all()
    paginator = Paginator(arcs, 10)  
    page_number = request.GET.get('page') 
    page_arcs = paginator.get_page(page_number) 
    return render(request,'WikiPage/arcs.html',{'page_title':'ARCOS DE ONE PIECE', 'arcs':page_arcs})
    
def chapter_list(request):
    chapters = Chapter.objects.all()
    paginator = Paginator(chapters, 10)  
    page_number = request.GET.get('page') 
    page_chapters = paginator.get_page(page_number) 
    return render(request, 'WikiPage/chapters.html',{'page_title':'CAPÍTULOS DE ONE PIECE',  'chapters':page_chapters})
    
def character(request,id): 
    character = get_object_or_404(Character, id=id)
    return render(request, 'WikiPage/character.html', {'page_title':character.name, 'character': character})
    
def saga_arcs(request, id):
    saga = get_object_or_404(Saga, id=id)
    # Obtener los arcos asociados con los capítulos de esta saga
    arcs = Arc.objects.filter(chapters__saga=saga).distinct()
    return render(request, 'WikiPage/arcs.html', {'page_title': f'Arcos de {saga.title}','saga': saga, 'arcs': arcs})
    
def saga_chapter(request, id):  
    saga = get_object_or_404(Saga, id=id) 
    chapters = Chapter.objects.filter(saga=saga)
    return render(request, 'WikiPage/chapter.html', {'page_title': f'Capítulos de {saga.title}','saga': saga, 'chapters': chapters})

def arc_chapter(request, id):  
    arc = get_object_or_404(Arc, id=id) 
    chapters = Chapter.objects.filter(arc=arc)
    return render(request, 'WikiPage/chapters.html', {'page_title': f'Capítulos de {arc.title}','arc': arc, 'chapters': chapters})
    
def character_fruit(request, id):  
    fruit = get_object_or_404(Fruit, id=id)
    characters = Character.objects.filter(fruit=fruit)
    return render(request, 'WikiPage/fruit.html', {'page_title': f'Fruta {fruit.name}', 'fruit':fruit, 'characters':characters})

def character_crew(request, id):  
    crew = get_object_or_404(Crew, id=id)
    characters = Character.objects.filter(crew=crew)
    return render(request, 'WikiPage/crew.html', {'page_title': f'Tripulación {crew.name}', 'crew':crew, 'characters':characters})

def global_search(request):  
     # Obtener el término de búsqueda desde la barra de navegación
    search_query = request.GET.get('nombre', '').strip()

    characters = []
    fruits = []
    crews = []
    sagas = []
    arcs = []
    chapters = []

    if search_query:
        # Realizar búsquedas simples usando Q para combinar filtros
        characters = Character.objects.filter(
            Q(name__icontains=search_query) |
            Q(fruit__name__icontains=search_query) |
            Q(job__icontains=search_query) | 
            Q(age__icontains=search_query) |
            Q(bounty__icontains=search_query)
        ).order_by('name') 

        fruits = Fruit.objects.filter(
            Q(name__icontains=search_query) |
            Q(roman_name__icontains=search_query) |
            Q(type__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by('name') 

        crews = Crew.objects.filter(
            Q(name__icontains=search_query) |
            Q(roman_name__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by('name') 

        sagas = Saga.objects.filter(
            Q(title__icontains=search_query) | 
            Q(saga_number__icontains=search_query)|
            Q(saga_volume__icontains=search_query)|
            Q(saga_chapitre__icontains=search_query)|
            Q(saga_episode__icontains=search_query)
        ).order_by('title') 

        arcs = Arc.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by('title') 
        
        chapters = Chapter.objects.filter(
            Q(title__icontains=search_query) |
            Q(number__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(chapter__icontains=search_query) | 
            Q(release_date__icontains=search_query) |
            Q(saga__title__icontains=search_query) | 
            Q(arc__title__icontains=search_query) 
        ).order_by('number') 
         
    all_results = list(characters) + list(fruits) + list(crews) + list(sagas) + list(arcs) + list(chapters)

    # Paginación: dividir los resultados en páginas
    paginator = Paginator(all_results, 10)  # Mostrar 10 resultados por página
    page_number = request.GET.get('page', 1)  # Obtener la página actual
    page_results = paginator.get_page(page_number)
    

    # Renderizar resultados
    return render(request, 'WikiPage/search.html', {
        'page_title': f'Resultados de búsqueda para: {search_query}',
        'search_query': search_query,
        'page_results': page_results,  
    }) 