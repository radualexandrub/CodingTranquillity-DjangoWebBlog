# Generated by Django 3.0.3 on 2020-08-30 07:57

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_auto_20200829_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('body', ckeditor.fields.RichTextField()),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('blogpost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='MainApp.BlogPost')),
            ],
        ),
    ]
