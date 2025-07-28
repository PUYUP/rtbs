import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from datetime import datetime, date, timedelta


class CustomUser(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True)

    def __str__(self):
        return self.email


class RestaurantTable(models.Model):
    tablenum = models.CharField(max_length=250)
    creationdate = models.DateTimeField(auto_now_add=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Table {self.tablenum} ({self.capacity} seats)"

    def is_available_at(self, datetime_check, duration_minutes=120):
        """Check if table is available at specific datetime"""
        end_time = datetime_check + timedelta(minutes=duration_minutes)
        conflicting_bookings = self.bookings.filter(
            booking_datetime__lt=end_time,
            booking_datetime__gt=datetime_check - timedelta(minutes=120),
            status__in=['confirmed', 'seated']
        ).exists()

        return not conflicting_bookings


class BookingSession(models.Model):
    DAYS_OF_WEEK = [
        'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday'
    ]

    tables = models.ManyToManyField(RestaurantTable, related_name='sessions', blank=True)
    session_name = models.CharField(max_length=50)  # e.g., 'Lunch', 'Dinner'
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=120, null=True, blank=True)  # typical booking duration
    buffer_minutes = models.PositiveIntegerField(default=15, null=True, blank=True)  # cleanup time
    max_bookings_per_slot = models.PositiveIntegerField(default=1, null=True, blank=True)
    days_of_week = models.JSONField(default=list, blank=True)  # ['monday', 'tuesday', ...]
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If days_of_week is empty, include all days
        if not self.days_of_week:
            self.days_of_week = self.DAYS_OF_WEEK
            super().save(update_fields=['days_of_week'])

        # delete existing time slots for this session
        TimeSlot.objects.filter(session=self).delete()

        # recreate time slots
        slots = self.generate_time_slots_without_date()
        for day in self.days_of_week:
            if not slots:
                TimeSlot.objects.create(
                    session=self,
                    day_of_week=day,
                )
            else:
                # Create time slots for each day of the week
                for slot_time in slots:
                    TimeSlot.objects.create(
                        session=self,
                        day_of_week=day,
                        start_time=slot_time,
                        end_time=(
                            datetime.combine(date.min, slot_time) +
                            timedelta(minutes=self.duration_minutes)
                        ).time()
                    )

    # def save(self, *args, **kwargs):
    #     # If this is a new session being created
    #     is_new = self._state.adding

    #     # Store old values if this is an update
    #     if not is_new:
    #         old_instance = BookingSession.objects.get(pk=self.pk)
    #         old_start_time = old_instance.start_time
    #         old_end_time = old_instance.end_time
    #         old_duration = old_instance.duration_minutes
    #         old_buffer = old_instance.buffer_minutes
    #         old_days = old_instance.days_of_week

    #     super().save(*args, **kwargs)

    #     # If days_of_week is empty, include all days
    #     if not self.days_of_week:
    #         self.days_of_week = self.DAYS_OF_WEEK
    #         super().save(update_fields=['days_of_week'])

    #     # Generate time slots for the next 30 days if this is a new session
    #     if is_new:
    #         today = timezone.now().date()
    #         end_date = today + timedelta(days=30)
    #         self.generate_time_slots(today, end_date)

    #     # Update existing time slots if session parameters changed
    #     elif (
    #         old_start_time != self.start_time or
    #         old_end_time != self.end_time or
    #         old_duration != self.duration_minutes or
    #         old_buffer != self.buffer_minutes or
    #         old_days != self.days_of_week
    #     ):
    #         # Delete future time slots
    #         future_date = timezone.now().date()
    #         self.time_slots.filter(slot_date__gte=future_date).delete()

    #         # Regenerate future time slots
    #         end_date = future_date + timedelta(days=30)
    #         self.generate_time_slots(future_date, end_date)

    def __str__(self):
        return f"{self.session_name} ({self.start_time}-{self.end_time})"

    def clean(self):
        if (self.start_time and self.end_time) and self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")

    def is_available_on_day(self, day_name):
        """Check if session is available on specific day"""
        if not self.days_of_week:  # Empty list means all days
            return True
        return day_name.lower() in [day.lower() for day in self.days_of_week]

    def generate_time_slots_without_date(self):
        """Generate time slots without dates, just time slots within session hours"""
        slots = []
        slot_time = self.start_time
        if not slot_time or not self.end_time:
            return slots

        while slot_time < self.end_time:
            slots.append(slot_time)
            # Move to next slot
            slot_time = (
                datetime.combine(date.min, slot_time) +
                timedelta(minutes=self.duration_minutes + self.buffer_minutes)
            ).time()

        return slots

    def generate_time_slots(self, date_range_start, date_range_end):
        """Generate time slots for given date range"""
        slots = []
        current_date = date_range_start

        while current_date <= date_range_end:
            day_name = current_date.strftime('%A').lower()

            if self.is_available_on_day(day_name):
                # Generate slots within the session
                slot_time = self.start_time
                while slot_time < self.end_time:
                    slot_datetime = timezone.make_aware(
                        datetime.combine(current_date, slot_time)
                    )

                    # Check if slot doesn't already exist
                    if not TimeSlot.objects.filter(
                        session=self,
                        start_time=slot_datetime
                    ).exists():
                        slot = TimeSlot.objects.create(
                            session=self,
                            slot_date=current_date,
                            start_time=slot_datetime,
                            end_time=slot_datetime + timedelta(minutes=self.duration_minutes)
                        )
                        slots.append(slot)

                    # Move to next slot
                    slot_time = (
                        datetime.combine(date.min, slot_time) +
                        timedelta(minutes=self.duration_minutes + self.buffer_minutes)
                    ).time()

            current_date += timedelta(days=1)

        return slots


class TableBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('phone', 'Phone'),
        ('walk_in', 'Walk-in'),
        ('app', 'Mobile App'),
        ('third_party', 'Third Party'),
    ]

    table = models.ForeignKey(
        'rtbsapp.RestaurantTable',
        on_delete=models.SET_NULL,
        related_name='bookings',
        null=True,
        blank=True
    )
    timeslot = models.ForeignKey(
        'rtbsapp.TimeSlot',
        on_delete=models.SET_NULL,
        related_name='bookings',
        null=True,
        blank=True
    )

    # Booking information
    booking_reference = models.CharField(
        max_length=20,
        unique=True, 
        editable=False,
        null=True,
    )
    bookingnumber = models.IntegerField(unique=True)
    noofguest = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1
    )
    bookingdate = models.DateField(editable=False, null=True)
    bookingtime = models.TimeField(editable=False, null=True)
    booking_datetime = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    special_requests = models.TextField(blank=True)
    remark = models.CharField(max_length=250, blank=True)
    remark_date = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(
        default=120,
        null=True,
        blank=True
    )  # typical booking duration

    # Customer information
    fullname = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phonenum = models.CharField(max_length=15, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Date when booking was made
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['booking_datetime']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return '({}) - {}'.format(self.bookingnumber, self.fullname)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()

        # Set booking_date and booking_time from booking_datetime
        if self.booking_datetime:
            self.bookingdate = self.booking_datetime.date()
            self.bookingtime = self.booking_datetime.time()

        super().save(*args, **kwargs)

    def generate_booking_reference(self):
        """Generate unique booking reference"""
        while True:
            reference = f"BK{uuid.uuid4().hex[:6].upper()}"
            if not TableBooking.objects.filter(booking_reference=reference).exists():
                return reference

    def clean(self):
        # Validate party size against table capacity
        if self.table and self.noofguest > self.table.capacity:
            raise ValidationError(
                f"Party size ({self.noofguest}) exceeds table capacity ({self.table.capacity})"
            )

        # Validate booking is not in the past
        if self.booking_datetime and self.booking_datetime <= timezone.now():
            raise ValidationError("Cannot book in the past")

    def cancel(self, reason=""):
        """Cancel the booking"""
        self.status = 'cancelled'
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save()

    def confirm(self):
        """Confirm the booking"""
        if self.status == 'pending':
            self.status = 'confirmed'
            self.save()

    def mark_seated(self):
        """Mark customer as seated"""
        if self.status == 'confirmed':
            self.status = 'seated'
            self.save()

    def complete(self):
        """Mark booking as completed"""
        if self.status == 'seated':
            self.status = 'completed'
            self.save()

    def mark_no_show(self):
        """Mark as no show"""
        if self.status in ['confirmed', 'seated']:
            self.status = 'no_show'
            self.save()

    @property
    def end_datetime(self):
        """Calculate booking end time"""
        return self.booking_datetime + timedelta(minutes=self.duration_minutes)

    def can_be_cancelled(self):
        """Check if booking can be cancelled"""
        if self.status in ['cancelled', 'completed', 'no_show']:
            return False

        # Allow cancellation up to 2 hours before booking
        cancellation_deadline = self.booking_datetime - timedelta(hours=2)
        return timezone.now() <= cancellation_deadline

    def mark_timeslot_unavailable(self):
        """Mark the associated timeslot as unavailable after booking confirmation"""
        if (
            self.timeslot and
            self.status == 'confirmed' and
            self.timeslot.start_time and
            self.timeslot.end_time
        ):
            self.timeslot.is_available = False
            self.timeslot.save()

            # Also update table availability
            if self.table:
                TableAvailability.objects.filter(
                    table=self.table,
                    timeslot=self.timeslot
                ).update(
                    is_available=False,
                    booking=self
                )

    def mark_timeslot_available(self):
        """Mark the associated timeslot as available again after booking cancellation/completion"""
        if self.timeslot and self.status in ['cancelled', 'completed', 'no_show']:
            self.timeslot.is_available = True
            self.timeslot.save()

            # Also update table availability
            if self.table:
                TableAvailability.objects.filter(
                    table=self.table,
                    timeslot=self.timeslot
                ).update(
                    is_available=True,
                    booking=None
                )


class TimeSlot(models.Model):
    session = models.ForeignKey(
        BookingSession,
        on_delete=models.CASCADE,
        related_name='timeslots',
        null=True,
        blank=True
    )
    slot_date = models.DateField(null=True, blank=True)
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['session', 'start_time', 'day_of_week']
        ordering = ['-day_of_week', 'start_time']

    def __str__(self):
        if self.session:
            if self.start_time:
                return f"{self.day_of_week} - {self.session.session_name} - {self.start_time.strftime('%H:%M')}"
            return f"{self.day_of_week} - {self.session.session_name}"
        return 'None'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Create availability records for this time slot
        if self.is_available:
            self.create_availability_records()

    def create_availability_records(self):
        for table in self.session.tables.filter(is_active=True):
            TableAvailability.objects.update_or_create(
                table=table,
                timeslot=self,
                day_of_week=self.day_of_week,
                defaults={
                    'availability_date': self.slot_date,
                    'start_time': self.start_time,
                    'end_time': self.end_time,
                    'is_available': True,
                }
            )

    def get_available_tables(self, noofguest=None):
        """Get available tables for this time slot"""
        tables = RestaurantTable.objects.filter(is_active=True)

        if noofguest:
            tables = tables.filter(capacity__gte=noofguest)

        available_tables = []
        for table in tables:
            if table.is_available_at(self.start_time, self.session.duration_minutes):
                available_tables.append(table)

        return available_tables


class TableAvailability(models.Model):
    table = models.ForeignKey(
        'rtbsapp.RestaurantTable',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='availabilities'
    )
    timeslot = models.ForeignKey(
        'rtbsapp.TimeSlot',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='availabilities'
    )
    availability_date = models.DateField(null=True, blank=True)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ],
        null=True,
        blank=True
    )
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    booking = models.ForeignKey(
        'rtbsapp.TableBooking',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            'table',
            'timeslot',
            'availability_date',
            'start_time',
            'end_time',
        ]
        indexes = [
            models.Index(fields=['availability_date', 'is_available']),
        ]

    def __str__(self):
        status = "Available" if self.is_available else "Booked"
        return f"{self.table} - {self.availability_date} {self.start_time} ({status})"


# Manager classes for common queries
class BookingManager(models.Manager):
    def today_bookings(self):
        queryset = self.filter(booking_date=timezone.now().date())
        return queryset.order_by('booking_time')

    def confirmed_bookings(self):
        return self.filter(status='confirmed')

    def by_status(self, status):
        return self.filter(status=status)

    def upcoming_bookings(self, days=7):
        end_date = timezone.now().date() + timedelta(days=days)
        return self.filter(
            booking_date__gte=timezone.now().date(),
            booking_date__lte=end_date,
            status__in=['confirmed', 'seated']
        )


# Add managers to models
TableBooking.add_to_class('objects', BookingManager())
