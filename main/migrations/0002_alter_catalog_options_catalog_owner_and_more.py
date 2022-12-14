# Generated by Django 4.1 on 2022-08-13 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalog',
            options={'ordering': ['-id'], 'verbose_name': 'Каталог'},
        ),
        migrations.AddField(
            model_name='catalog',
            name='owner',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='catalog',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photo'),
        ),
    ]
