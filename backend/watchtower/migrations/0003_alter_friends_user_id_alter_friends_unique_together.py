# Generated by Django 5.1.5 on 2025-02-14 02:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchtower', '0002_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='friendships', to='watchtower.user'),
        ),
        migrations.AlterUniqueTogether(
            name='friends',
            unique_together={('user_id', 'friend_id')},
        ),
    ]
