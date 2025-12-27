"""road_sense URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login/', views.login),
    path('login_post/', views.login_post),
    path('change_password/', views.change_password),
    path('change_pswd_post/', views.change_pswd_post),
    path('logout/', views.logout),
    path('Admin_home/', views.Admin_home),

    path('manage_ev/', views.manage_evStations),
    path('search_Ev/', views.search_Ev),
    path('Approve_ev_statn/<did>', views.Approve_ev),
    path('approved_ev/', views.Approved_stations),
    path('Search_Apprved_ev/', views.Search_Apprved_ev),
    path('Reject_ev_statn/<did>', views.Reject_ev),
    path('rejected_ev/', views.RejectedStations),
    path('Search_Rjctd_ev/', views.Search_Rjctd_ev),

    path('manage_workers/',views.manage_workers),
    path('Search_workers/',views.Search_workers),
    path('verify_wrkr/<did>',views.verify_worker),
    path('verifyed_workers/',views.verifyed_workers),
    path('Search_vrfyd_workers/',views.Search_vrfyd_workers),
    path('Reject_wrkr/<did>',views.reject_worker),
    path('Rejeced_workers/',views.Rejected_workers),
    path('Search_Rjctd_workers/',views.Search_Rjctd_workers),

    path('view_fuel_station/', views.view_fuel_station),
    path('view_fuel_station_post/', views.view_fuel_station_post),
    path('Approve_fuel/<did>', views.Approve_fuel),
    path('Approved_fuel_stations/', views.Approved_fuel_stations),
    path('Approved_fuel_stations_post/', views.Approved_fuel_stations_post),
    path('Reject_fuel/<did>', views.Reject_fuel),
    path('Rejected_fuel_Stations/', views.Rejected_fuel_Stations),
    path('Rejected_fuel_Stations_post/', views.Rejected_fuel_Stations_post),

    path('view_user_complaint_nd_reply/',views.view_user_complaint_nd_reply),
    path('Search_User_comp/',views.Search_User_comp),
    path('send_user_reply/<did>',views.reply_user_com),
    path('send_usr_rply_post/',views.send_reply_post_user),
    path('view_review_rating/',views.view_review_rating),
    path('view_review_rating_post/',views.view_review_rating_post),




    #=============Ev station==============================

    path('Evstnhome/', views.home),

    path('signin/', views.signin),
    path('sigin_post_ev/', views.Signin_post),

    path('change_password_ev/', views.change_password_ev),
    path('change_pswd_post_ev/', views.change_pswd_post_ev),

    path('ev_profile/', views.ev_profile),
    path('ed_edit_profile/', views.ed_edit_profile),
    path('ed_edit_profile_post/', views.ed_edit_profile_post),

    path('add_charging_point/',views.add_charging_point),
    path('add_charging_point_post/',views.add_charging_point_post),
    path('view_charging_point/',views.view_charging_point),
    path('view_charging_point_post/',views.view_charging_point_post),
    path('edit_charging_point/<id>',views.edit_charging_point),
    path('edit_charging_point_post/',views.edit_charging_point_post),
    path('delete_charging_point/<id>',views.delete_charging_point),

    path('Addslot/', views.Addslot),
    path('Addslot_post/', views.Addslot_post),
    path('View_slot/', views.View_slot),
    path('Search_slots/', views.Search_slots),
    path('delete_slot/<did>', views.delete_slot),
    path('edit_slot/<did>', views.edit_slot),
    path('Edit_slot_post/', views.Edit_slot_post),

    path('view_slot_booked/', views.view_slot_booked),
    path('ev_view_booking/<id>', views.ev_view_booking),
    path('ev_view_booking_post/', views.ev_view_booking_post),
    path('ev_view_payment/', views.ev_view_payment),
    path('ev_view_payment_post/', views.ev_view_payment_post),


    path('approve_slots/<did>', views.approve_slots),
    path('reject_slots/<did>', views.reject_slots),
    path('Search_booked_slots/', views.Search_booked_slots),
    path('View_Approved_slots/', views.View_Approved_slots),
    path('Approved_slot_search/', views.Approved_slot_search),
    path('View_Rejected_slots/', views.View_Rejected_slots),
    path('Rejected_slot_search/', views.Rejected_slot_search),

    path('View_users/', views.View_users),
    path('search_view_users/', views.search_view_users),

    path('ev_view_review/', views.ev_view_review),
    path('ev_view_review_post/', views.ev_view_review_post),

    # path('Send_complaints/', views.Send_complaints),
    # path('Send_comp_post/', views.Send_comp_post),
    # path('View_reply/', views.View_reply),
    # path('Search_View_reply/', views.Search_View_reply),
    #
    # path('View_general_feedback/', views.View_general_feedback),
    # path('Search_general_feed/', views.Search_general_feed),
    path('view_user_feedback/', views.view_user_feedback),
    path('Search_user_feed/', views.Search_user_feed),


    #=========Fuel Station================================

    path('fs_email_exist/',views.fs_email_exist),
    path('f_register/',views.f_register),
    path('f_register_post/',views.f_register_post),

    path('fs_home/',views.fs_home),
    path('fs_profile/',views.fs_profile),
    path('active_work_status/<id>',views.active_work_status),
    path('deactive_work_status/<id>',views.deactive_work_status),

    path('fs_edit_profile/',views.fs_edit_profile),
    path('fs_edit_profile_post/',views.fs_edit_profile_post),
    path('fs_change_password/',views.fs_change_password),
    path('fs_change_pswd_post/',views.fs_change_pswd_post),

    path('fs_add_stock/',views.fs_add_stock),
    path('fs_add_stock_post/',views.fs_add_stock_post),
    path('fs_view_stock/',views.fs_view_stock),
    path('fs_delete_stock/<id>',views.fs_delete_stock),
    path('fs_view_bookings/',views.fs_view_bookings),

    path('fs_view_review/',views.fs_view_review),
    path('fs_view_review_post/',views.fs_view_review_post),

    #=========Worker===========================================

    path('and_login/',views.and_login),


    path('worker_signup_post/',views.worker_signup_post),
    path('worker_view_profile/',views.worker_view_profile),
    path('worker_edit_profile/',views.worker_edit_profile),
    path('w_add_service/',views.w_add_service),
    path('w_view_service/',views.w_view_service),
    path('w_delete_service/',views.w_delete_service),
    path('worker_view_service_request/',views.worker_view_service_request),
    path('worker_approve_request/',views.worker_approve_request),
    path('worker_reject_request/',views.worker_reject_request),
    path('worker_view_approved_service_request/',views.worker_view_approved_service_request),
    path('worker_view_rejected_service_request/',views.worker_view_rejected_service_request),
    path('worker_view_service_review/',views.worker_view_service_review),

    path('worker_sendchat/',views.worker_sendchat),
    path('worker_viewchat/',views.worker_viewchat),
    path('worker_change_password/',views.worker_change_password),
    path('w_view_payment/',views.w_view_payment),


    #===========Users==============================================

    path('user_signup_post/',views.user_signup_post),
    path('user_view_profile/',views.user_view_profile),
    path('user_edit_profile/',views.user_edit_profile),
    path('user_view_evstation/',views.user_view_evstation),
    path('get_nearest_ev/',views.get_nearest_ev),
    path('user_view_charging_slot/',views.user_view_charging_slot),
    path('user_view_charging_point/',views.user_view_charging_point),
    path('user_book_ev_slot/',views.user_book_ev_slot),
    path('user_view_ev_bookings/',views.user_view_ev_bookings),
    path('user_send_ev_review/', views.user_send_ev_review),
    path('user_view_ev_review/', views.user_view_ev_review),

    path('user_view_fuelstation/',views.user_view_fuelstation),
    path('get_nearest_fs/',views.get_nearest_fs),
    path('user_view_fuelstock/',views.user_view_fuelstock),
    path('user_book_fuel/',views.user_book_fuel),
    path('user_view_fuel_booking/',views.user_view_fuel_booking),
    path('user_view_fs_review/',views.user_view_fs_review),
    path('user_send_fs_review/',views.user_send_fs_review),

    path('user_view_service/',views.user_view_service),
    # path('get_nearest_worker/',views.get_nearest_worker),
    path('u_send_service_request/',views.u_send_service_request),
    path('user_view_service_request/',views.user_view_service_request),
    path('user_service_payment/',views.user_service_payment),
    path('user_send_service_review/',views.user_send_service_review),
    path('user_view_service_review/',views.user_view_service_review),
    path('User_sendchat/',views.User_sendchat),
    path('User_viewchat/',views.User_viewchat),


    path('_update_location/',views._update_location),
    path('user_appreview_post/',views.user_appreview_post),
    path('user_view_appreview_post/',views.user_view_appreview_post),
    path('user_view_complaint_post/',views.user_view_complaint_post),
    path('user_send_complaint/',views.user_send_complaint),






]
