CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.fields.ImageField', {}],
}

CONSTANCE_CONFIG = {
    'LOGO_IMAGE': ('', 'A logo for this website', 'image_field'),
    'TAGLINE': ('Resturant Table Booking System', 'Change website tagline', str),
    'BACKGROUND_IMAGE': ('', 'Change background image webpage', 'image_field'),
    'BACKGROUND_COLOR_BOOKING_FORM': ('', 'Booking form background color', str),
}
