# Generated by Django 3.1.4 on 2021-03-25 01:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('GET', 'GET'), ('HEAD', 'HEAD'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('CONNECT', 'CONNECT'), ('OPTION', 'OPTION'), ('TRACE', 'TRACE'), ('PATCH', 'PATCH')], default='GET', max_length=20, verbose_name='Request type')),
                ('url', models.URLField(verbose_name='URL')),
                ('headers', models.TextField(blank=True, help_text='Please use key:value pairs, one header per line', null=True, verbose_name='Headers')),
                ('params', models.TextField(blank=True, help_text='Specify the URL parameters to be used for the request, please use key:value pairs, one header per line', null=True, verbose_name='URL parameters')),
                ('data', models.TextField(blank=True, help_text='Data submitted in the body payload, please use key:value pairs, one header per line', null=True, verbose_name='Data')),
                ('scheduled_time', models.DateTimeField(db_index=True, verbose_name='Scheduled time')),
                ('response', models.TextField(null=True, verbose_name='Response data')),
                ('request_status', models.CharField(choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('FAILURE', 'Failure')], default='PENDING', max_length=20, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
