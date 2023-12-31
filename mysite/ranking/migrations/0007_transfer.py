# Generated by Django 4.2.7 on 2023-11-29 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0006_attendancehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transfer_amount', models.IntegerField()),
                ('remark', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_received', to='ranking.student')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers_sent', to='ranking.student')),
            ],
        ),
    ]
