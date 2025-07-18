# Generated by Django 5.2.3 on 2025-07-18 20:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("conference", "0006_finalregistration_fee_breakdown"),
    ]

    operations = [
        migrations.AddField(
            model_name="finalregistration",
            name="transaction_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="finalregistration",
            name="transaction_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="finalregistration",
            name="transaction_time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
