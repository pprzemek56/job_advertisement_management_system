# Generated by Django 4.1.7 on 2023-03-19 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_company_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='nip_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
