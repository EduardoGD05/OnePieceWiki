from django.contrib import admin

# Register your models here.  
from .models import Crew, Fruit, Character, Saga, Arc, Chapter

admin.site.register(Crew)
admin.site.register(Fruit)  
admin.site.register(Character) 
admin.site.register(Saga) 
admin.site.register(Arc) 
admin.site.register(Chapter) 
