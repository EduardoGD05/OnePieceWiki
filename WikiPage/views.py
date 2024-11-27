from django.shortcuts import render ,get_object_or_404  
# Create your views here.
from .models import Crew, Fruit, Character, Saga, Arc, Chapter

def home(request):
    return render(request,'WikiPage/onepiece.html')

def crew_list(request):
    crews = Crew.objects.all()
    return render(request,'WikiPage/crews.html',{'crews':crews})

def fruits_list(request):
    fruits =Fruit.objects.all()
    return render(request,'WikiPage/fruits.html',{'fruits':fruits})
    
def character_list(request):
    characters = Character.objects.all()
    return render(request,'WikiPage/characters.html',{'characters':characters})
    
def saga_list (request):
    sagas = Saga.objects.all()
    return render(request, 'WikiPage/sagas.html', {'sagas':sagas})
    
def arc_list(request):
    arcs = Arc.objects.all()
    return render(request,'WikiPage/arcs.html',{'arcs':arcs})
    
def chapter_list(request):
    chapters = Chapter.objects.all()
    return render(request, 'WikiPage/chapters.html',{'chapters':chapters})




    
def character(request,id): 
    character = get_object_or_404(Character, id=id)
    return render(request, 'WikiPage/character.html', {'character': character})
    

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
        'search_query': search_query,
        'characters': characters,
        'fruits': fruits,
        'crews': crews,
        'sagas': sagas,
        'arcs': arcs,
    })