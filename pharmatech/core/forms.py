from django.forms import ModelForm, Select
from django.urls import reverse_lazy
from pharmatech.core.models import Drug, Category
from django_addanother.widgets import AddAnotherWidgetWrapper, AddAnotherEditSelectedWidgetWrapper


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class DrugForm(ModelForm):
    class Meta:
        model = Drug
        exclude = ['']
        widgets = {
            'category': AddAnotherEditSelectedWidgetWrapper(Select, reverse_lazy('core:category_create'),
                                                            reverse_lazy('core:category_update', args=['__fk__']))
        }


class DrugUpdateForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['price']


class AddDrugForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['quantity']
