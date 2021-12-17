# Generated by Django 4.0 on 2021-12-16 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Agendador', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresa',
            old_name='razaoSocial',
            new_name='nome_fantasia',
        ),
        migrations.AddField(
            model_name='empresa',
            name='razao_social',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cnpj',
            field=models.IntegerField(),
        ),
    ]
