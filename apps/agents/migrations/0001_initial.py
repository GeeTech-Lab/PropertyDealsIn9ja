# Generated by Django 4.1.2 on 2023-10-19 12:42

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('business_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='agent', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('business_name', models.CharField(blank=True, max_length=150, null=True)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='business_name', unique_with=('date_registered',))),
                ('business_email', models.EmailField(blank=True, max_length=150, null=True)),
                ('business_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('business_logo', models.ImageField(blank=True, null=True, upload_to='agent_photos')),
                ('t_and_c', models.BooleanField(default=True)),
                ('agent_active', models.BooleanField(default=True)),
                ('is_an_agency', models.BooleanField(default=False)),
                ('agency_description', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=150, null=True)),
                ('land_mark_area', models.CharField(blank=True, max_length=150, null=True)),
                ('street_address', models.CharField(blank=True, max_length=150, null=True)),
                ('date_registered', models.DateTimeField(auto_now_add=True)),
                ('rating_aggregate', models.CharField(blank=True, default='0', max_length=100, null=True)),
                ('agency_agents', models.ManyToManyField(blank=True, related_name='agency_agents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, help_text='1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent')),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_review', to='agents.agent')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AgentMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_content', models.TextField(blank=True, null=True)),
                ('msg_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent_msg', to='agents.agent')),
                ('msg_from', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['msg_on'],
            },
        ),
    ]
