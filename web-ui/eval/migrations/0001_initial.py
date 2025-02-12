# Generated by Django 3.1.12 on 2025-01-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromptParam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.IntegerField()),
                ('eval_query', models.CharField(max_length=255)),
                ('eval_response', models.CharField(max_length=255)),
                ('ground_truth', models.CharField(max_length=255)),
                ('status', models.CharField(default='Pending', max_length=255)),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
