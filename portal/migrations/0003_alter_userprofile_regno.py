# Generated by Django 5.1.6 on 2025-02-22 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0002_rename_allusers_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="RegNo",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
