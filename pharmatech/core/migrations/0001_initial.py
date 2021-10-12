# Generated by Django 3.1.13 on 2021-10-12 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Entrez le nom de la catégorie', max_length=150, verbose_name='Nom')),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Entrez le nom du produit', max_length=150, unique=True, verbose_name='Nom')),
                ('price', models.PositiveIntegerField(verbose_name='Prix')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantité')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drug', to='core.category', verbose_name='Catégorie')),
            ],
        ),
    ]