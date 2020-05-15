# Generated by Django 3.0.6 on 2020-05-15 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAlmuerzos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendario',
            old_name='fecha_id',
            new_name='fecha',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='calendario_fecha_id',
            new_name='calendario',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='empleado_empleado_id',
            new_name='empleado',
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='menu_menu_id',
            new_name='menu',
        ),
        migrations.AddField(
            model_name='menu',
            name='nora',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionAlmuerzos.Nora'),
        ),
        migrations.AlterUniqueTogether(
            name='pedido',
            unique_together={('empleado', 'calendario')},
        ),
    ]