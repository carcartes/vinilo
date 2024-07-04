# Generated by Django 5.0.6 on 2024-07-01 00:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0002_pedido_tarjeta_caducidad_pedido_tarjeta_cvv_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pedido',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='tarjeta_caducidad',
            field=models.CharField(max_length=5),
        ),
    ]
