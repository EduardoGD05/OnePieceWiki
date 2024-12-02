from django.shortcuts import render ,get_object_or_404  
# Create your views here.
from .models import Crew, Fruit, Character, Saga, Arc, Chapter

def home(request):
    return render(request,'WikiPage/onepiece.html',{'page_title': 'CATEGORÍAS'})

def crew_list(request):
    crews = Crew.objects.all()
    return render(request,'WikiPage/crews.html',{'page_title':'TRIPULACIONES DE ONE PIECE', 'crews':crews})

def fruits_list(request):
    fruits =Fruit.objects.all()
    return render(request,'WikiPage/fruits.html',{'page_title':'FRUTAS DEL DIABLO', 'fruits':fruits})
    
def character_list(request):
    characters = Character.objects.all()
    return render(request,'WikiPage/characters.html',{'page_title':'PERSONAJES', 'characters':characters})
    
def saga_list (request):
    sagas = Saga.objects.all()
    return render(request, 'WikiPage/sagas.html', {'page_title':'SAGAS DE ONE PIECE', 'sagas':sagas})
    
def arc_list(request):
    arcs = Arc.objects.all()
    return render(request,'WikiPage/arcs.html',{'page_title':'ARCOS DE ONE PIECE', 'arcs':arcs})
    
def chapter_list(request):
    chapters = Chapter.objects.all()
    return render(request, 'WikiPage/chapters.html',{'page_title':'CAPÍTULOS DE ONE PIECE',  'chapters':chapters})




    
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

def global_search(request):
    # Obtener el término de búsqueda desde la barra de navegación
    search_query = request.GET.get('nombre', '').strip()

    # Inicializar resultados
    characters = []
    fruits = []
    crews = []
    sagas = []
    arcs = []

    if search_query:
        # Realizar búsqueda en cada modelo
        characters = Character.objects.filter(name__icontains=search_query)
        fruits = Fruit.objects.filter(name__icontains=search_query)
        crews = Crew.objects.filter(name__icontains=search_query)
        sagas = Saga.objects.filter(title__icontains=search_query)
        arcs = Arc.objects.filter(title__icontains=search_query)

    # Pasar los resultados al template
    return render(request, 'WikiPage/search.html', {
        'page_title': f'Resultados de busqueda para:  "{search_query}"',
        'search_query': search_query,
        'characters': characters,
        'fruits': fruits,
        'crews': crews,
        'sagas': sagas,
        'arcs': arcs,
    })