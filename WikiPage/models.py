from django.db import models
from django.contrib.auth.models import User


class Crew(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=200, default='Desconocido')
    number = models.IntegerField()
    roman_name = models.CharField(max_length=100)
    total_prime = models.CharField(max_length=100)
    is_yonko = models.BooleanField()
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Fruit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50)
    filename = models.CharField(max_length=100)
    roman_name = models.CharField(max_length=100)
    technicalFile = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=200,default='Desconocido')
    size = models.CharField(max_length=50, default='Desconocido')
    birthday = models.CharField(max_length=50, default='Desconocido')
    age = models.CharField(max_length=50)
    bounty = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=200, default='Desconocido')
    crew = models.ForeignKey(Crew, on_delete=models.SET_NULL, null=True)
    fruit = models.ForeignKey(Fruit, on_delete=models.SET_NULL, null=True)
    image_url = models.URLField(null=True, blank=True) 

    def __str__(self):
        return self.name
        
# PARA LAS SAGAS

class Saga(models.Model):
    title = models.CharField(max_length=255)
    saga_number = models.CharField(max_length=100)
    saga_chapitre = models.CharField(max_length=100)
    saga_volume = models.CharField(max_length=100)
    saga_episode = models.CharField(max_length=100)
    image_url = models.URLField(null=True, blank=True) 

    def __str__(self):
        return self.title

# ARCOS

class Arc(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(null=True, blank=True) 

    def __str__(self):
        return self.title

# PARA LOS CAPÍTULOS

class Chapter(models.Model):
    number = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    chapter = models.CharField(max_length=100)
    release_date = models.DateField()

    # Relaciones con Saga y Arc
    saga = models.ForeignKey(Saga, related_name='chapters', on_delete=models.CASCADE)
    arc = models.ForeignKey(Arc, related_name='chapters', on_delete=models.CASCADE)
    image_url = models.URLField(null=True, blank=True) 

    def __str__(self):
        return f"{self.title} (Capítulo {self.number})"
    

    # WIKI
class Page(models.Model):
    title = models.CharField(max_length=255)
    main_image_url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Section(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255, default="Sin título")
    content = models.TextField()
    type = models.CharField(max_length=50, choices=[('text', 'Texto'), ('image', 'Imagen'), ('video', 'Video')])
    order = models.PositiveIntegerField(default=0)  # Campo para ordenar las secciones

    class Meta:
        ordering = ['order']  # Ordenar por el campo 'order'

    def __str__(self):
        return f"{self.title} ({self.type})"