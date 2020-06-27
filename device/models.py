from django.db import models

# Create your models here.
class Device(models.Model):
    uid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag = models.IntegerField(default=1)

    class Meta:
        db_table = "device"

class TemperatureReadings(models.Model):
    tid = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    reading = models.FloatField(default=0.0)
    starts_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    ends_at = models.DateTimeField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "temperature_readings"

class HumidityReadings(models.Model):
    hid = models.BigAutoField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    reading = models.FloatField(default=0.0)
    starts_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    ends_at = models.DateTimeField(default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "humidity_readings"
