# Generated by Django 4.2 on 2023-05-26 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gfournisseur', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fournisseur',
            name='email',
        ),
    ]
