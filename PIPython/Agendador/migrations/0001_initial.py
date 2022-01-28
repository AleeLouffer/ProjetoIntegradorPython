# Generated by Django 4.0 on 2022-01-14 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Login', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('preco', models.FloatField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('telefone', models.CharField(max_length=11)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dataEHora', models.DateField(null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agendador.cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.empresa')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agendador.funcionario')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agendador.servico')),
            ],
        ),
    ]
