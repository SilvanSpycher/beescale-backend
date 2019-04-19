# Generated by Django 2.2 on 2019-04-19 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scale',
            name='settings',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scale', to='scales.Setting'),
        ),
    ]