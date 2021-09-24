# Generated by Django 3.2.7 on 2021-09-24 10:21

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
            name='LoyaltyPoint',
            fields=[
                ('totalPoints', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='LoyaltyPointTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionPoints', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('transactionType', models.CharField(choices=[('accrew', 'Accrew'), ('redeem', 'Redeem')], max_length=50)),
                ('transactionRestaurant', models.CharField(choices=[('mbuzi munch lavington', 'Mbuzi Munch Lavington'), ('mbuzi munch naivasha', 'Mbuzi Munch Naivasha'), ('mbuzi munch galleria', 'Mbuzi Munch Galleria')], max_length=50)),
                ('transactionPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('redeemedAt', models.DateTimeField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('loyaltyPoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loyalty_point.loyaltypoint')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]