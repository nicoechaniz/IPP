import autocomplete_light.shortcuts as al
from .models import ProductoConMarca

al.register(ProductoConMarca,
    search_fields=['marca',],
    attrs={
        'placeholder': '...',
        'data-autocomplete-minimum-characters': 2,
    },
)
