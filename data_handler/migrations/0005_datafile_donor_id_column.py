# Generated by Django 3.0.7 on 2020-07-02 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_handler', '0004_datafile_selected_columns_dtypes'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='donor_id_column',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
