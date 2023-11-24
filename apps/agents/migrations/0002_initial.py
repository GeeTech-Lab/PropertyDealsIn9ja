# Generated by Django 4.1.2 on 2023-11-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enquiries', '0001_initial'),
        ('agents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='my_paid_enquiries',
            field=models.ManyToManyField(blank=True, related_name='agent_enquiries', to='enquiries.enquiry'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'agent')},
        ),
    ]
