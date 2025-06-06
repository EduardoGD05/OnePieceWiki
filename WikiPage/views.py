from django.shortcuts import render, get_object_or_404, redirect  
from .models import Crew, Fruit, Character, Saga, Arc, Chapter, Page, Section
from django.db.models import Q,Exists, OuterRef
import re
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def home(request):
    return render(request,'WikiPage/onepiece.html',{'page_title': ''})
 
def crew_list(request):
    crews = Crew.objects.all()
    for crew in crews:
     crew.exists = Page.objects.filter(title=crew.name).exists()
    paginator = Paginator(crews, 10)  
    page_number = request.GET.get('page') 
    page_crews = paginator.get_page(page_number) 
    return render(request,'WikiPage/crews.html',{'page_title':'TRIPULACIONES DE ONE PIECE', 'crews':page_crews})

def fruits_list(request):
    fruits =Fruit.objects.all() 
    for fruit in fruits:
        fruit.exists = Page.objects.filter(title=fruit.name).exists()
    paginator = Paginator(fruits, 10)  
    page_number = request.GET.get('page') 
    page_fruits = paginator.get_page(page_number) 
    return render(request,'WikiPage/fruits.html',{'page_title':'FRUTAS DEL DIABLO', 'fruits':page_fruits})
    
def character_list(request):
    characters = Character.objects.all()
    for character in characters:
        character.exists = Page.objects.filter(title=character.name).exists()
        character.crew.exists = Page.objects.filter(title=character.crew.name).exists() if character.crew else False
        character.fruit.exists = Page.objects.filter(title=character.fruit.name).exists() if character.fruit else False

    paginator = Paginator(characters, 10)
    page_number = request.GET.get('page')
    page_characters = paginator.get_page(page_number)

    return render(request, 'WikiPage/characters.html', {'page_title': 'PERSONAJES', 'characters': page_characters})
    
def saga_list (request):
    sagas = Saga.objects.all() 
    for saga in sagas:
        saga.exists = Page.objects.filter(title=saga.title).exists()
    return render(request, 'WikiPage/sagas.html', {'page_title':'SAGAS DE ONE PIECE', 'sagas':sagas})
    
def arc_list(request):
    arcs = Arc.objects.all()
    for arc in arcs:
        arc.exists = Page.objects.filter(title=arc.title).exists()
    paginator = Paginator(arcs, 10)  
    page_number = request.GET.get('page') 
    page_arcs = paginator.get_page(page_number) 
    return render(request,'WikiPage/arcs.html',{'page_title':'ARCOS DE ONE PIECE', 'arcs':page_arcs})
    
def chapter_list(request):
    chapters = Chapter.objects.all() 
    for chapter in chapters:
        chapter.exists = Page.objects.filter(title=chapter.title).exists()
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
    
    # Obtener los títulos ya existentes en el modelo Page
    existing_titles = Page.objects.values_list('title', flat=True)

    # Agregar un atributo "exists" a cada personaje
    for character in characters:
        character.exists = character.name in existing_titles

    # Renderizar resultados
    return render(request, 'WikiPage/search.html', {
        'page_title': f'Resultados de búsqueda para: {search_query}',
        'search_query': search_query,
        'page_results': page_results,  
    }) 
def view_page(request, page_name):
    page = get_object_or_404(Page, title=page_name)
    return render(request, 'WikiPage/view_page.html', {
        'page': page
    })

# Asegúrate de que las redirecciones en otras funciones utilicen el título de la página.
# Por ejemplo:
# return redirect('view_page', page_name=page.title)

def check_page_exists(request):
    title = request.GET.get('title', '').strip()
    exists = Page.objects.filter(title=title).exists()
    return JsonResponse({'exists': exists})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('/')  # Redirect to the homepage or another page
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return redirect('login') 
    return render(request,'WikiPage/login.html',{'page_title': 'Login'})
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('signup')

        # Crear el usuario
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
        return redirect('login')

    return render(request,'WikiPage/signup.html',{'page_title': 'Signup'})

@login_required
def create_page(request):
    # Obtener el título desde los parámetros GET o POST
    title = request.POST.get('title', request.GET.get('title', '').strip())

    if request.method == 'POST':
        # Si el título no está definido, mostrar un error
        if not title:
            messages.error(request, "El título de la página es obligatorio.")
            return redirect('create_page')

        # Crear la página
        main_image_url = request.POST.get('main_image_url', '').strip()

        # Crear la página en la base de datos con el usuario autenticado
        page = Page.objects.create(
            title=title,
            main_image_url=main_image_url,
            created_by=request.user,  # Asignar el usuario autenticado
        )

        # Obtener las listas de datos del formulario
        section_ids = request.POST.getlist('section_ids[]')  # IDs de las secciones
        section_titles = request.POST.getlist('module_titles[]')  # Títulos de las secciones
        section_contents = request.POST.getlist('module_contents[]')  # Contenidos de las secciones

        # Depuración: Imprimir los datos enviados
        print("section_ids:", section_ids)
        print("section_titles:", section_titles)
        print("section_contents:", section_contents)

        # Verifica que las listas tengan el mismo tamaño
        if len(section_ids) != len(section_contents):
            messages.error(request, "Error: Los datos enviados no son consistentes.")
            page.delete()  # Eliminar la página si hay un error
            return redirect('create_page')

        # Procesar las secciones
        for index, section_id in enumerate(section_ids):
            # Verificar que el índice exista en las otras listas
            if index >= len(section_contents):
                continue

            content = section_contents[index].strip()
            title = section_titles[index].strip() if index > 0 else "main"  # La primera sección siempre es "main"

            # Ignorar secciones sin contenido
            if not content:
                continue

            # Crear una nueva sección
            Section.objects.create(
                page=page,
                title=title,
                content=content,
                order=index,  # Usar el índice como orden
                type='text',  # Tipo fijo como "text"
            )

        messages.success(request, "Página creada exitosamente.")
        return redirect('view_page', page_name=page.title)

    # Pasar el título al contexto
    return render(request, 'WikiPage/create_page.html', {
        'title': title if title else "Título por Defecto",  # Usar un título predeterminado si no se proporciona
        'range': range(5)  # Pasar un rango para nuevas secciones
    })

def search_titles(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        # Obtener los títulos ya existentes en el modelo Page
        existing_titles = Page.objects.values_list('title', flat=True)

        # Buscar en los modelos relevantes y excluir los títulos existentes
        characters = Character.objects.filter(name__icontains=query).exclude(name__in=existing_titles).values('id', 'name')
        fruits = Fruit.objects.filter(name__icontains=query).exclude(name__in=existing_titles).values('id', 'name')
        crews = Crew.objects.filter(name__icontains=query).exclude(name__in=existing_titles).values('id', 'name')
        sagas = Saga.objects.filter(title__icontains=query).exclude(title__in=existing_titles).values('id', 'title')
        arcs = Arc.objects.filter(title__icontains=query).exclude(title__in=existing_titles).values('id', 'title')
        chapters = Chapter.objects.filter(title__icontains=query).exclude(title__in=existing_titles).values('id', 'title')

        # Combinar los resultados y agregar display_name
        results = (
            list(characters) +
            list(fruits) +
            list(crews) +
            [{'id': saga['id'], 'display_name': saga['title']} for saga in sagas] +
            [{'id': arc['id'], 'display_name': arc['title']} for arc in arcs] +
            [{'id': chapter['id'], 'display_name': chapter['title']} for chapter in chapters]
        )

        # Agregar display_name para los resultados con 'name'
        for result in results:
            if 'name' in result:
                result['display_name'] = result['name']

    return render(request, 'WikiPage/search_titles.html', {
        'page_title': 'Buscar Títulos',
        'query': query,
        'results': results
    }) 
 
@login_required  
def edit_page(request, page_name):
    page = get_object_or_404(Page, title=page_name)

    if request.method == 'POST':
        page.main_image_url = request.POST.get('main_image_url', page.main_image_url)
        page.save()

        section_ids = request.POST.getlist('section_ids[]')
        section_titles = request.POST.getlist('module_titles[]')  # Solo para las secciones no "main"
        section_contents = request.POST.getlist('module_contents[]')

        if len(section_ids) != len(section_contents):
            messages.error(request, "Error: Los datos enviados no son consistentes.")
            return redirect('edit_page', page_name=page.title)

        title_index = 0
        seen_main = False

        existing_section_ids = set(str(s.id) for s in page.sections.all())
        received_ids = set(section_ids)
        sections_to_delete = existing_section_ids - received_ids

        for i, section_id in enumerate(section_ids):
            content = section_contents[i].strip()
            if not content:
                continue

            if section_id.startswith("new-"):
                # Crear sección nueva
                # Asumimos que el primer campo oculto (sin título visible) es "main"
                if not seen_main:
                    title = "main"
                    seen_main = True
                else:
                    title = section_titles[title_index].strip() if title_index < len(section_titles) else "Sin título"
                    title_index += 1

                Section.objects.create(
                    page=page,
                    title=title,
                    content=content,
                    order=i,
                    type='text',
                )
            else:
                try:
                    section = Section.objects.get(id=section_id, page=page)
                    if section.title == "main":
                        seen_main = True
                        title = "main"
                    else:
                        title = section_titles[title_index].strip() if title_index < len(section_titles) else section.title
                        title_index += 1

                    if section.title != title or section.content != content or section.order != i:
                        section.title = title
                        section.content = content
                        section.order = i
                        section.save()
                except Section.DoesNotExist:
                    continue

        # Eliminar secciones removidas por el usuario
        if sections_to_delete:
            Section.objects.filter(id__in=sections_to_delete, page=page).delete()

        messages.success(request, "Página actualizada exitosamente.")
        return redirect('view_page', page_name=page.title)

    return render(request, 'WikiPage/edit_page.html', {'page': page})
