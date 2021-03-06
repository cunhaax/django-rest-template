# Generated by Django 2.0.1 on 2018-01-12 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_auto_20180112_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.TextField(choices=[('made', 'made'), ('missed', 'missed')])),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='loan',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AddField(
            model_name='payment',
            name='loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.Loan'),
        ),
    ]
