# Generated by Django 5.0.7 on 2024-10-28 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financas_online', '0013_alter_financas_arquivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financas',
            name='arquivo',
            field=models.FileField(blank=True, null=True, upload_to='media/comprovantes'),
        ),
    ]
