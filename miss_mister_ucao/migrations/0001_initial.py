# Generated by Django 5.1.5 on 2025-02-13 07:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Miss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='miss_photos/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('miss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='miss_mister_ucao.miss')),
            ],
        ),
    ]
