# Generated by Django 5.0.7 on 2024-08-01 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cursos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curso', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=50)),
                ('nascimento', models.DateField()),
                ('registro', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='financas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_ori', models.CharField(max_length=50)),
                ('cliente', models.CharField(max_length=100)),
                ('parcela', models.CharField(max_length=100)),
                ('valor', models.CharField(max_length=100)),
                ('curso', models.CharField(max_length=50)),
                ('turma', models.CharField(max_length=50)),
                ('data', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='turmas_formatec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turmas_formatec', models.CharField(max_length=40)),
            ],
        ),
    ]
