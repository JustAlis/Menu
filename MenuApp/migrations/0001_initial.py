# Generated by Django 4.1.7 on 2023-05-04 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('menu_name', models.CharField(max_length=255, verbose_name='menu_name')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='menu_url')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_parent', to='MenuApp.menu')),
            ],
        ),
    ]
