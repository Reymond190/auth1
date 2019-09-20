from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from app_auth.views import device_listview,devicelistview
from .views import travel_summary,detail_travel_summary,trip_summary,\
    stoppage_summary,idle_summary,idle_detail_summary,inactive_summary,\
    ignition_summary,ac_summary,ac_misused_summary,speed_vs_distance,\
    vehicle_location,sms_email,vehicle_status,system_log,report_generator,device_log,\
    analog_data,personal_report,rfid_data,actual_trip_summary

urlpatterns = [
    path('travel_summary/', travel_summary, name='travel'),
    path('detail_travel_summary/', detail_travel_summary, name='detail_travel'),
    path('trip_summary/', trip_summary, name='trip_summary'),
    path('stoppage_summary/', stoppage_summary, name='stoppage_summary'),
    path('idle_detail_summary/', idle_detail_summary, name='idle_detail_summary'),
    path('inactive_summary/', inactive_summary, name='inactive_summary'),
    path('ignition_summary/', ignition_summary, name='ignition_summary'),
    path('ac_summary/', ac_summary, name='ac_summary'),
    path('ac_misused_summary/', ac_misused_summary, name='ac_misused_summary'),
    path('idle_summary/', idle_summary, name='idle_summary'),
    path('speed_vs_distance/', speed_vs_distance, name='speed_vs_distance'),
    path('vehicle_location/', vehicle_location, name='vehicle_location'),
    path('sms_email/', sms_email, name='sms_email'),
    path('vehicle_status/', vehicle_status, name='vehicle_status'),
    path('system_log/', system_log, name='system_log'),
    path('report_generator/', report_generator, name='report_generator'),
    path('device_log/', device_log, name='device_log'),
    path('analog_data/', analog_data, name='analog_data'),
    path('personal_report/', personal_report, name='personal_report'),
    path('rfid_data/', rfid_data, name='rfid_data'),
    path('actual_trip_summary/',actual_trip_summary, name='actual_trip_summary'),



]