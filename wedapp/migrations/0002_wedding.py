# Generated by Django 3.1.1 on 2020-09-24 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wedapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wedding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wedder_one', models.CharField(max_length=60)),
                ('wedder_two', models.CharField(max_length=60)),
                ('wedding_date', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guests', models.ManyToManyField(related_name='weddings_attended', to='wedapp.User')),
                ('planner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weddings_planned', to='wedapp.user')),
            ],
        ),
    ]
