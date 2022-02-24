# Generated by Django 4.0 on 2022-02-20 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Login', '0001_initial'),
        ('Agendador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forma_de_Pagamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=30)),
                ('ativo', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Contas_a_Receber',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.FloatField()),
                ('desconto', models.FloatField()),
                ('juros', models.FloatField()),
                ('total', models.FloatField()),
                ('pago', models.BooleanField(default=False)),
                ('data_de_pagamento', models.DateField(null=True)),
                ('data_de_vencimento', models.DateField()),
                ('data_de_emissao', models.DateField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('agendamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agendador.agendamento')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.empresa')),
                ('forma_de_pagamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Contas_a_Receber.forma_de_pagamento')),
            ],
        ),
    ]
