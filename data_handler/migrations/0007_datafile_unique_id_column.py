# Generated by Django 3.0.7 on 2020-07-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_handler', '0006_datafile_is_donor_id_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='unique_id_column',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
