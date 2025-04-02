from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='highlight_all')
def highlight_all(obj, query):
    if not query or not obj:
        return obj
    escaped_query = re.escape(query)
    
    # Comprobar si obj es un objeto y recorrer sus campos de texto
    if hasattr(obj, "__dict__"):
        for field, value in obj.__dict__.items():
            if isinstance(value, str):
                setattr(obj, field, highlight_matches(value, escaped_query))
    
    # Si obj no es un objeto, asumir que es texto
    if isinstance(obj, str):
        return highlight_matches(obj, escaped_query)
    
    return obj

def highlight_matches(text, query):
    print(f"Text: {text}, Query: {query}")  # Verificar si está recibiendo los valores correctos
    highlighted_text = re.sub(
        f'({query})',
        r'<span class="highlight">\1</span>',
        text,
        flags=re.IGNORECASE
    )
    print(f"Highlighted text: {highlighted_text}")  # Verificar el texto resaltado
    return mark_safe(highlighted_text)
    
@register.filter
def get_type(value):
    return type(value).__name__