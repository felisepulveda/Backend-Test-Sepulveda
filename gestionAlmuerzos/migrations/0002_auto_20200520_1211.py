# Generated by Django 3.0.6 on 2020-05-20 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAlmuerzos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='customizacion',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
