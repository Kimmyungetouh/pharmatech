from django.contrib import messages
import xlrd
from tablib import Dataset
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView
# Create your views here.
from django_addanother.views import CreatePopupMixin, UpdatePopupMixin

from pharmatech.core.forms import DrugForm, CategoryForm, DrugUpdateForm, AddDrugForm
from pharmatech.core.models import Drug, Category


class CatalogueView(ListView):
    model = Drug
    template_name = 'pages/catalogue/index.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data(**kwargs)
        context['drug_list'] = Drug.objects.all()
        context['form'] = DrugForm
        context['drug_update_form'] = DrugUpdateForm
        context['drug_add_form'] = AddDrugForm
        return context

    def post(self, request):
        form = DrugForm(request.POST)
        if form.is_valid():
            if Drug.objects.filter(name__iexact=form.instance.name).exists():
                drug = Drug.objects.filter(name__iexact=form.instance.name)
                print(drug.quantity)
                drug.quantity += form.instance.quantity
                print(form.instance.quantity)
                print(drug.quantity)
                drug.save()
                messages.success(request, "%s existe déjà, un ajout de stock a été effectué !" % drug.name)
            else:
                form.save()
                messages.success(request, "Enregistrement de %s effectué avec succès !" % form.instance.name)
        else:
            print("*** form is not valid ***")
            print(form.errors)
        return redirect(reverse('core:catalogue'))


class CreateCategoryView(CreatePopupMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "pages/category/create.html"


class UpdateCategoryView(UpdatePopupMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "pages/category/update.html"


class CreateDrugView(CreateView):
    model = Drug
    form_class = DrugForm
    template_name = 'pages/drug/create.html'


class UpdateDrugView(UpdateView):
    model = Drug
    fields = ['price']

    def get_success_url(self):
        return reverse('core:catalogue')


class AddDrugView(UpdateView):
    model = Drug
    fields = ['quantity']

    def form_valid(self, form):
        drug = self.get_object()
        drug.quantity += form.instance.quantity
        drug.save()
        return redirect(reverse('core:catalogue'))

    def get_success_url(self) -> str:
        messages.success(self.request, "Succès !")
        return reverse('core:catalogue')


class AddvDrugView(UpdateView):
    model = Drug
    fields = ['quantity']

    def form_valid(self, form):
        drug = self.get_object()
        drug.quantity += form.instance.quantity
        drug.save()
        return redirect(reverse('core:catalogue'))

    def get_success_url(self) -> str:
        messages.success(self.request, "Succès !")
        return reverse('core:vente')


class SellDrugView(UpdateView):
    model = Drug
    fields = ['quantity']

    def form_valid(self, form):
        drug = self.get_object()
        quantity = drug.quantity
        if quantity < form.instance.quantity:
            messages.error(self.request, "Vous n'avez pas autant de %s !" % drug.name)
            return redirect(reverse('core:vente'))
        drug.quantity -= form.instance.quantity
        drug.save()
        return redirect(reverse('core:vente'))

    def get_success_url(self) -> str:
        messages.success(self.request, "Succès !")
        return reverse('core:catalogue')


def check_name(request):
    name = request.GET.get('name', None)
    data = {
        'exist': Drug.objects.filter(name__iexact=name).exists()
    }

    return JsonResponse(data)


class VenteView(ListView):
    model = Drug
    template_name = "pages/catalogue/vente.html"

    def get_context_data(self, **kwargs):
        context = super(VenteView, self).get_context_data(**kwargs)
        context['drug_list'] = Drug.objects.all()
        context['drug_update_form'] = DrugUpdateForm
        context['drug_add_form'] = AddDrugForm
        return context


class UploadDrugListView(View):

    def post(self, request, **kwargs):
        fic = request.FILES['drug_list']
        try:
            drugs = Dataset().load(fic, headers=['№', 'Catégorie', 'Nom du produit', 'Prix', 'Quantité', 'Actions'])
            for drug in drugs.dict:
                if Drug.objects.filter(name__iexact=drug.get('Nom du produit').strip()).exists():
                    pass
                else:
                    if not Category.objects.filter(name__iexact=drug.get('Catégorie')).exists():
                        cat = Category.objects.create(name=drug.get('Catégorie'))
                        Drug.objects.create(name=drug.get('Nom du produit').strip(),
                                            category_id=cat.id,
                                            price=drug.get('Prix').strip(),
                                            quantity=drug.get('Quantité').strip()
                                            )
                    else:
                        cat = Category.objects.get(name=drug.get('Catégorie'))
                        Drug.objects.create(name=drug.get('Nom du produit').strip(),
                                            category_id=cat.id,
                                            price=drug.get('Prix').strip(),
                                            quantity=drug.get('Quantité').strip()
                                            )
            messages.success(request, "Liste des produits chargée avec succès !")
            return redirect(reverse('core:catalogue'))

        except Exception as e:
            print(e)
            messages.error(request,
                           "Échec dans le chargement de la list de produit ! Si le problème persiste, veuillez "
                           "procéder manuellement")
            return redirect(reverse('core:catalogue'))
