# Generated by Django 3.0.7 on 2020-07-02 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_handler', '0005_datafile_donor_id_column'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='is_donor_id_selected',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
