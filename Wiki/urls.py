from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from WikiPage import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.global_search, name='global_search'),
    path('crews/', views.crew_list, name='crews'), 
    path('crews/<int:id>/', views.character_crew, name='crew'), 
    path('characters/', views.character_list, name='characters'), 
    path('character/<int:id>/', views.character, name='character'),
    path('fruits/<int:id>/', views.character_fruit, name='fruit'),
    path('fruits/', views.fruits_list, name='fruits'),  
    path('sagas/', views.saga_list, name='sagas'),
    path('saga/<int:id>/arcs/', views.saga_arcs, name='saga_arcs'),
    path('saga/<int:id>/chapters/', views.saga_chapter, name='saga_chapter'),   
    path('arcs/', views.arc_list, name='arcs'),
    path('arc/<int:id>/chapters/', views.arc_chapter, name='arc_chapter'),
    path('chapters/', views.chapter_list, name='chapters'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), 
    path('create-page/', views.create_page, name='create_page'),
    path('search-titles/', views.search_titles, name='search_titles'),
    path('page/<str:page_name>/', views.view_page, name='view_page'),
    path('page/<str:page_name>/edit/', views.edit_page, name='edit_page'),
    path('api/check-page-exists/', views.check_page_exists, name='check_page_exists')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)