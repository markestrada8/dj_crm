# Generated by Django 4.2.4 on 2024-02-11 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0006_category_lead_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="leads.userprofile",
            ),
        ),
    ]
