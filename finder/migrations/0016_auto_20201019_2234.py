# Generated by Django 3.1.1 on 2020-10-20 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finder', '0015_auto_20201019_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='graduation',
            field=models.CharField(choices=[('', ''), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030')], default='', max_length=100, null=True),
        ),
    ]