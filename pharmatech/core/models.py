from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom", help_text="Entrez le nom de la catégorie")

    def __str__(self):
        return "%s" % self.name


class Drug(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom", help_text="Entrez le nom du produit", unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="drug", verbose_name="Catégorie", help_text="Cliquez sur les icones pour plus d'actions")
    price = models.PositiveIntegerField(verbose_name="Prix")
    # available = models.BooleanField(default=True, verbose_name="Disponible")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")

    def __str__(self):
        return "%s - %s -" % (self.name, self.category)

    @property
    def qr_code(self):
        return "%s -- %s -- %s XOF -- %s restant(s)" % (self.name, self.category.name, self.price, self.quantity)


