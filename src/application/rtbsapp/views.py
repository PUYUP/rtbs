from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rtbsapp.models import CustomUser, Resturanttable, Tablebooking
import random
from datetime import date
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.utils.timezone import timedelta

User = get_user_model()


def BASE(request):
    return render(request, 'base.html')


def Index(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phonenum = request.POST.get("phonenum")
        bookingdate = request.POST.get("bookingdate")
        noofguest = request.POST.get("noofguest")
        bookingtime = request.POST.get("bookingtime")

        # Convert bookingdate to a date object
        booking_date_obj = date.fromisoformat(bookingdate)
        bookingnumber = random.randint(100000000, 999999999)

        # Prevent booking for past dates
        if booking_date_obj < date.today():
            messages.error(request, "You cannot book a table for a past date. Please select a future date.")
            return redirect("index")

        # Save to the database
        booking = Tablebooking.objects.create(
            fullname=fullname,
            email=email,
            phonenum=phonenum,
            bookingdate=booking_date_obj,
            noofguest=int(noofguest),
            bookingtime=bookingtime,
            status="pending",
            bookingnumber=bookingnumber,
        )
        booking.save()

        # Display success message with the integer booking number
        messages.success(request, f"Your reservation has been submitted! Your booking number is: {booking.bookingnumber}")

        return redirect("index")  # Redirect to homepage after submission
    return render(request, "index.html")


def LOGIN(request):
    return render(request, 'login.html')


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        new_password = request.POST.get('newpassword')

        try:
            user = CustomUser.objects.get(email=email, mobile=mobile)
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            messages.success(request, "Your password has been successfully changed.")
            return redirect('login')  # Redirect to login page
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid email or mobile number.")
    return render(request, 'reset_password.html')


def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        try:
            user = authenticate(request, username=username, password=password)
        except Exception as e:
            print(e)

        if user is not None:
            if user.is_superuser:  # Ensure the user is an admin
                login(request, user)
                return redirect('dashboard')  # Redirect to admin dashboard
            else:
                messages.error(request, 'Access denied: Only admin accounts are allowed.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # Redirect back to login page
    else:
        messages.error(request, 'Invalid request method')
        return redirect('login')


def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')


@login_required(login_url='/Login')
def CalendarPage(request):
    context = {}
    return render(request, 'calendar-page.html', context)


@login_required(login_url='/Login')
def ADMIN_PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/Login')
def DASHBOARD(request):
    table_count = Resturanttable.objects.all().count
    allbooking_count = Tablebooking.objects.all().count()
    newbooking_count = Tablebooking.objects.filter(status='pending').count()
    abooking_count = Tablebooking.objects.filter(status='Accepted').count()
    rbooking_count = Tablebooking.objects.filter(status='Rejected').count()
    context = {
        'table_count': table_count,
        'newbooking_count': newbooking_count,
        'abooking_count': abooking_count,
        'rbooking_count': rbooking_count,
        'allbooking_count': allbooking_count,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='/Login')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobnum = request.POST.get('mobnum')
        print(profile_pic)

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.email = email
            customuser.mobile = mobnum           

            if profile_pic is not None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()

            print(customuser.profile_pic.path)
            messages.success(request, "Your profile has been updated successfully")
            return redirect('admin_profile')
        except Exception as e:
            print(e)
            messages.error(request, "Your profile updation has been failed")
    return render(request, 'profile.html')


@login_required(login_url='/Login')
def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)

    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context.update({'data': data})

    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check:
            user.set_password(new_pas)
            user.save()
            messages.success(request, 'Password Change  Succeesfully!!!')
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.error(request, 'Current Password wrong!!!')
            return redirect("change_password")
    return render(request, 'change-password.html')


@login_required(login_url='/Login')
def Add_Table(request):
    if request.method == "POST":
        tableno_value = request.POST.get('tableno')
        if tableno_value:
            try:
                type_obj = Resturanttable(tablenum=tableno_value)
                type_obj.save()
                messages.success(request, "Table  detail has been created successfully")
                return redirect('add_table')
            except IntegrityError:
                messages.error(request, "This table number already exists.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please provide a valid table number.")
    return render(request, 'add-table.html')


@login_required(login_url='/Login')
def MANAGE_TABLE(request):
    type_list = Resturanttable.objects.all()
    paginator = Paginator(type_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        tablenum = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tablenum = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tablenum = paginator.page(paginator.num_pages)

    context = {'tablenum': tablenum}
    return render(request, 'manage-table.html', context)


@login_required(login_url='/Login')
def DELETE_TABLE(request, id):
    tablenum = Resturanttable.objects.get(id=id)
    tablenum.delete()
    messages.success(request, 'Record Delete Succeesfully!!!')

    return redirect('manage_table')


@login_required(login_url='/Login')
def New_Booking(request):
    booking_list = Tablebooking.objects.filter(status='Pending')
    paginator = Paginator(booking_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        booking = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        booking = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        booking = paginator.page(paginator.num_pages)

    context = {'booking': booking}
    return render(request, 'new-booking.html', context)


@login_required(login_url='/Login')
def VIEW_BOOKING(request, id):
    view_booking = Tablebooking.objects.filter(id=id)
    table_num = Resturanttable.objects.all()

    context = {
        'view_booking': view_booking,
        'table_num': table_num,
    }
    return render(request, 'view-booking-details.html',context)


@login_required(login_url='/Login')
def ALL_Booking(request):
    booking_list = Tablebooking.objects.all()
    paginator = Paginator(booking_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        booking = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        booking = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        booking = paginator.page(paginator.num_pages)

    context = {'booking': booking}
    return render(request, 'new-booking.html', context)


@login_required(login_url='/Login')
def Accepted_Booking(request):
    booking_list = Tablebooking.objects.filter(status='Accepted')
    paginator = Paginator(booking_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        booking = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        booking = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        booking = paginator.page(paginator.num_pages)

    context = {'booking': booking}
    return render(request, 'new-booking.html', context)


@login_required(login_url='/Login')
def Rejected_Booking(request):
    booking_list = Tablebooking.objects.filter(status='Rejected')
    paginator = Paginator(booking_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        booking = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        booking = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        booking = paginator.page(paginator.num_pages)

    context = {'booking': booking}
    return render(request, 'new-booking.html', context)


@login_required(login_url='/Login')
def UPDATE_BOOKING_REMARK(request):
    if request.method == "POST":
        booking_id = request.POST.get('bid')
        remark_text = request.POST.get('remark')
        status_text = request.POST.get('status')
        table_id = request.POST.get('table')
        booking_date = request.POST.get('bdate')  # Example: "2025-02-21"
        booking_time = request.POST.get('btime')  # Example: "14:30"

        try:
            # Fetch booking instance
            booking_update = get_object_or_404(Tablebooking, id=booking_id)

            # Convert `booking_date` to Python `date` format
            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()

            # Convert `booking_time` to Python `time` format
            booking_time_obj = datetime.strptime(booking_time, "%H:%M").time()

            # Calculate end time (+30 minutes)
            end_time = (datetime.combine(booking_date_obj, booking_time_obj) + timedelta(minutes=30)).time()

            # Check table availability if status is "Accepted"
            if table_id and status_text == "Accepted":
                table_instance = get_object_or_404(Resturanttable, id=int(table_id))

                overlapping_bookings = Tablebooking.objects.filter(
                    table_id=table_instance,
                    bookingdate=booking_date_obj,
                    status="Accepted"
                ).filter(
                    bookingtime__gte=booking_time_obj, bookingtime__lt=end_time
                )

                if overlapping_bookings.exists():
                    messages.error(request, "Table already booked for the given date and time. Please choose another table.")
                    return redirect('all_booking')

                # Assign table if available
                booking_update.table_id = table_instance

            # Update booking details
            booking_update.remark = remark_text
            booking_update.status = status_text
            booking_update.bookingdate = booking_date_obj
            booking_update.bookingtime = booking_time_obj
            booking_update.remark_date = timezone.now()
            booking_update.save()

            messages.success(request, "Booking status updated successfully.")
        except ValueError:
            messages.error(request, "Invalid date or time format. Please enter correct values.")
        except Tablebooking.DoesNotExist:
            messages.error(request, "Booking not found.")
        except Resturanttable.DoesNotExist:
            messages.error(request, "Selected table does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('all_booking')


@login_required(login_url='/Login')
def Booking_Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    tb = []
    error_message = None

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date > end_date:
                error_message = 'Start date cannot be after end date.'
            else:
                tb = Tablebooking.objects.filter(postingdate__range=(start_date, end_date))
                if not tb:
                    error_message = 'No bookings found for the selected date range.'
        except ValueError:
            error_message = 'Invalid date format. Please use YYYY-MM-DD.'

    return render(
        request,
        'between-dates-booking-report.html',
        {
            'tb': tb,
            'start_date': start_date,
            'end_date': end_date,
            'error_message': error_message,
        }
    )


@login_required(login_url='/Login')
def Search_Booking(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            tb = Tablebooking.objects.filter(
                bookingnumber__icontains=query
            )

            messages.success(request, f"Search results for '{query}'")
            return render(
                request,
                'search-booking.html',
                {
                    'tb': tb,
                    'query': query
                }
            )
        else:
            return render(request, 'search-booking.html', {})


def Check_Booking_Status(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            tb = Tablebooking.objects.filter(
                bookingnumber__icontains=query
            )

            messages.success(request, f"Search results for '{query}'")
            return render(
                request,
                'booking-status.html',
                {
                    'tb': tb,
                    'query': query
                }
            )
        else:
            return render(request, 'booking-status.html', {})


def VIEW_BOOKING_STATUS(request, bookingnumber):
    view_booking_status = Tablebooking.objects \
        .filter(bookingnumber=bookingnumber)
    context = {
         'view_booking_status':view_booking_status,
    }
    return render(request, 'view-booking-status-details.html', context)
