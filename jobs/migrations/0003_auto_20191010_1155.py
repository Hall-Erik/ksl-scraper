# Generated by Django 2.2.6 on 2019-10-10 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20191006_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-date_posted', 'employer', 'name']},
        ),
        migrations.RemoveField(
            model_name='searchpattern',
            name='user',
        ),
        migrations.AlterField(
            model_name='searchpattern',
            name='pattern',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]