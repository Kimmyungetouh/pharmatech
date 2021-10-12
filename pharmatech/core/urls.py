from django.urls import path
from pharmatech.core.views import (CatalogueView,
                                   CreateCategoryView, UpdateCategoryView,
                                   CreateDrugView, UpdateDrugView, AddDrugView, AddvDrugView,
                                    check_name, VenteView, SellDrugView
                                   )

app_name = "core"
urlpatterns = [
    path('catalogue', CatalogueView.as_view(), name="catalogue"),
    path('category/new', CreateCategoryView.as_view(), name="category_create"),
    path('category/update/<pk>', UpdateCategoryView.as_view(), name="category_update"),
    path('drug/create/', CreateDrugView.as_view(), name="drug_create"),
    path('drug/update/<pk>', UpdateDrugView.as_view(), name="drug_update"),
    path('drug/add/<pk>', AddDrugView.as_view(), name="drug_add"),
    path('drug/addv/<pk>', AddvDrugView.as_view(), name="drug_addv"),
    path('drug/sell/<pk>', SellDrugView.as_view(), name="drug_sell"),

    path('vente', VenteView.as_view(), name="vente"),
    path('check_name', check_name, name="check_name")
]
