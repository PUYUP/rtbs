
from django.urls import path, include
from .import views

urlpatterns = [
    path('base/', views.BASE, name='base'),
    path('Dashboard', views.DASHBOARD, name='dashboard'),
    path('', views.Index, name='index'),
    path('Login', views.LOGIN, name='login'),
    path('ResetPassword', views.reset_password, name='reset_password'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('AdminProfile', views.ADMIN_PROFILE, name='admin_profile'),
    path('AdminProfile/update', views.ADMIN_PROFILE_UPDATE, name='admin_profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),
    path('AddTable', views.Add_Table, name='add_table'),
    path('ManageTable', views.MANAGE_TABLE, name='manage_table'),
    path('DeleteTable/<str:id>', views.DELETE_TABLE, name='delete_table'),
    path('NewBooking', views.New_Booking, name='new_booking'),
    path('AllBooking', views.ALL_Booking, name='all_booking'),
    path('AcceptedBooking', views.Accepted_Booking, name='accepted_booking'),
    path('RejectedBooking', views.Rejected_Booking, name='rejected_booking'),
    path('ViewBooking/<str:id>', views.VIEW_BOOKING, name='view-booking'),
    path('UpdateBookingRemark', views.UPDATE_BOOKING_REMARK, name='update-booking-remark'),
    path('BookingBetweenDateReport', views.Booking_Between_Date_Report, name='booking-bwdate-report'),
    path('SearchBooking', views.Search_Booking, name='search_booking'),
    path('CheckBookingStatus', views.Check_Booking_Status, name='check_booking_status'),
    path('ViewBookingStatus/<str:bookingnumber>/', views.VIEW_BOOKING_STATUS, name='view_booking_status'),
    path('Calendar', views.CalendarPage, name='calendar-page'),

    path('api/', include(('rtbsapp.api.urls', 'api'), namespace='api')),
]
