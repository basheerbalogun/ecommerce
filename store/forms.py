
from django.forms import ModelForm

from .models import Product


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        field = '__all__'
        exclude = ('user', 'status', 'slug',)


