# Generated by Django 5.1.7 on 2025-03-18 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ['price', 'departure_time']},
        ),
        migrations.RemoveField(
            model_name='flight',
            name='aircraft',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='baggage_allowance',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='booking_url',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='flight_number',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='refundable',
        ),
        migrations.AddField(
            model_name='flight',
            name='from_location',
            field=models.CharField(default='NYC', max_length=3),
        ),
        migrations.AddField(
            model_name='flight',
            name='to_location',
            field=models.CharField(default='LAX', max_length=3),
        ),
        migrations.AlterField(
            model_name='flight',
            name='arrival_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='flight',
            name='departure_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='flight',
            name='duration',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='flight',
            name='stops',
            field=models.CharField(max_length=50),
        ),
    ]
