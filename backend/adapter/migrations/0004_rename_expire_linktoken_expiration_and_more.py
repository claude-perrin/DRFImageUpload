# Generated by Django 4.0.5 on 2022-06-23 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adapter', '0003_linktoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linktoken',
            old_name='expire',
            new_name='expiration',
        ),
        migrations.AlterField(
            model_name='linktoken',
            name='token',
            field=models.CharField(default='8a5fb44715f319425ed7b5ca4dcd7e473ff3651b', max_length=20),
        ),
    ]