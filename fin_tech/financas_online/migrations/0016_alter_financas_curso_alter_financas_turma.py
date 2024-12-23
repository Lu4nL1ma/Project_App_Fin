# Generated by Django 5.0.7 on 2024-11-12 00:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financas_online', '0015_alter_financas_arquivo_alter_financas_curso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financas',
            name='curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financas_online.cursos'),
        ),
        migrations.AlterField(
            model_name='financas',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='financas_online.turmas_formatec'),
        ),
    ]
