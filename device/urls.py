from django.urls import path
from device import views

urlpatterns = [ 
    path('api/devices/', views.IotDevice.as_view()),
    path('api/devices/<int:id>', views.IotDevice.as_view()),
    path('api/devices/<int:id>', views.IotDevice.as_view()),
    path('api/devices/', views.DeviceListing.as_view()),
    path('api/devices/<int:id>/readings/<str:parameter>/', views.PeriodTemperature.as_view()),
    path('get/temperature/', views.GetTemperature.as_view()),
    path('get/humidity/', views.GetHumidity.as_view()),
]
