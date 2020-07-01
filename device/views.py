# Django Imports
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND
from django.db.models import Q

# Misc
import datetime
import traceback

# Model Imports
from device.models import Device, TemperatureReadings, HumidityReadings

# Create your views here.

# CRUD API for IOT device
class IotDevice(APIView):
    # API for creating device
    @staticmethod
    def post(request):
        try:
            name = request.POST.get("name")
            device_obj = Device.objects.create(name=name)
            res = {
                "message": "Device Created Successfully",
                "status": HTTP_201_CREATED,
                "device detail": {"uid": device_obj.uid, "name": device_obj.name},
            }
            return Response(res, res["status"])
        except:
            res = {"message": traceback.format_exc(), "status": HTTP_500_INTERNAL_SERVER_ERROR, "result": {}}
            return Response(res, res["status"])

    # API for deleting device
    @staticmethod
    def delete(request, id):
        try:
            if not Device.objects.filter(uid=id):
                return Response({"message": "Invalid ID"}, status.HTTP_404_NOT_FOUND)
            Device.objects.filter(uid=id).delete()
            return Response({"result": {"message": "Device Deleted."}})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # API to retrieve a device
    @staticmethod
    def get(request, id):
        device_details = Device.objects.filter(uid=id).values.first()
        temperature_list = TemperatureReadings.objects.filter(device_id=id).values_list("readings")
        humidity_list = TemperatureReadings.objects.filter(device_id=id).values_list("readings")
        return Response(
            {
                "result": {
                    "device_details": device_details,
                    "device_temp_list": temperature_list,
                    "device_humidity_list": humidity_list,
                }
            },
            status=status.HTTP_200_OK,
        )

# API for listing all devices
class DeviceListing(APIView):
    @staticmethod
    def get(request):
        try:
            search = request.GET.get("search", None)
            device_details = Device.objects.filter().values()

            if search:
                device_details = Device.objects.filter(Q(uid__icontains=search) | Q(name__icontains=search)).values()

            res = {"message": "Devices detail fetched successfully", "status": HTTP_200_OK, "result": device_details}
            return Response(res, res["status"])
        except:
            res = {"message": traceback.format_exc(), "status": HTTP_500_INTERNAL_SERVER_ERROR, "result": {}}
            return Response(res, res["status"])

# Api for getting temperature readings from the frontend and storing it corrosponsing to device.
# This API should be called after every 10 sec.
class GetTemperature(APIView):
    @staticmethod
    def post(request):
        try:
            uid = request.POST.get("uid")
            reading = request.POST.get("reading")
            if not uid and reading:
                res = {"message": "Request param missing", "status": status.HTTP_400_BAD_REQUEST, "result": []}
                return Response(res, res["status"])
            tempobj = TemperatureReadings.objects.create(device_id=uid, reading=reading)
            tempobj.ends_at = tempobj.starts_at + datetime.timedelta(seconds=10)
            tempobj.save()
            res = {"message": "Temperature updated Successfully", "status": status.HTTP_201_CREATED}
            return Response(res, res["status"])
        except:
            res = {"message": traceback.format_exc(), "status": HTTP_500_INTERNAL_SERVER_ERROR, "result": {}}
            return Response(res, res["status"])

# Api for getting humidity readings from the frontend and storing it corrosponsing to device.
# This API should be called after every 10 sec.
class GetHumidity(APIView):
    @staticmethod
    def post(request):
        try:
            uid = request.POST.get("uid")
            reading = request.POST.get("reading")
            if not uid and reading:
                res = {"message": "Request param missing", "status": status.HTTP_400_BAD_REQUEST, "result": []}
                return Response(res, res["status"])
            humobj = HumidityReadings.objects.create(device_id=uid, reading=reading)
            humobj.ends_at = humobj.starts_at + datetime.timedelta(seconds=10)
            humobj.save()
            res = {"message": "Humidity updated Successfully", "status": status.HTTP_201_CREATED}
            return Response(res, res["status"])
        except:
            res = {"message": traceback.format_exc(), "status": HTTP_500_INTERNAL_SERVER_ERROR, "result": {}}
            return Response(res, res["status"])

#API for getting temperature or humidity in given range of time
class PeriodTemperature(APIView):
    @staticmethod
    def get(request, id, parameter):
        start_on = request.GET.get("start_on")
        end_on = request.GET.get("end_on")
        if parameter == "Temperature":
            tempobj = TemperatureReadings.objects.filter(device_id=id).first()
            if tempobj.starts_at > end_on:
                return Response({"message": "No readings between this time period"}, HTTP_404_NOT_FOUND)
            if start_on <= tempobj.starts_at:
                result = TemperatureReadings.objects.filter(ends_at=[tempobj.ends_at, end_on]).values()
            if start_on > tempobj.starts_at:
                start_time = start_on + datetime.timedelta(seconds=10)
                result = TemperatureReadings.objects.filter(ends_at=[start_time, end_on]).values()

        if parameter == "Humidity":
            tempobj = HumidityReadings.objects.filter(device_id=id).first()
            if tempobj.starts_at > end_on:
                return Response({"message": "No readings between this time period"}, HTTP_404_NOT_FOUND)
            if start_on <= tempobj.starts_at:
                result = HumidityReadings.objects.filter(ends_at=[tempobj.ends_at, end_on]).values()
            if start_on > tempobj.starts_at:
                start_time = start_on + datetime.timedelta(seconds=10)
                result = HumidityReadings.objects.filter(ends_at=[start_time, end_on]).values()
        return Response({"Result": result}, HTTP_200_OK)

