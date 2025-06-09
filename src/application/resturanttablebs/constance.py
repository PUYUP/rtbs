from django.utils.translation import gettext_lazy as _

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.fields.ImageField', {'required': False}],
    'file_field': ['django.forms.fields.FileField', {'required': False}],
}

CONSTANCE_CONFIG = {
    'LOGO_IMAGE': ('', _('A logo for this website'), 'image_field'),
    'TAGLINE': ('Resturant Table Booking System', _('Change website tagline'), str),

    'NAVBAR_BACKGROUND_COLOR': ('#ffffff', _('Change navbar background color'), str),
    'NAVBAR_TEXT_COLOR': ('#333333', _('Change navbar text color'), str),
    'FOOTER_BACKGROUND_COLOR': ('#222222', _('Change footer background color'), str),
    'FOOTER_TEXT_COLOR': ('#ffffff', _('Change footer text color'), str),

    'BACKGROUND_IMAGE': ('', _('Change background image webpage'), 'image_field'),
    'BACKGROUND_COLOR_BOOKING_FORM': ('', _('Booking form background color'), str),
    'MANU_PAGE_CONTENT': ('', _('Can be PDF or image file.'), 'file_field'),
    'MANU_PDF_BACKGROUND_COLOR': ('#333', _('Change PDF file background color.'), str),

    'BUTTON_BACKGROUND_COLOR': ('#f36700', _('Change button background color'), str),
    'BUTTON_HOVER_COLOR': ("#c05000", _('Change button hover background color'), str),
    'BUTTON_TEXT_COLOR': ('#ffffff', _('Change button text color'), str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'General': ('BACKGROUND_IMAGE', 'FOOTER_BACKGROUND_COLOR', 'FOOTER_TEXT_COLOR', ),
    'Navbar': ('LOGO_IMAGE', 'TAGLINE', 'NAVBAR_BACKGROUND_COLOR', 'NAVBAR_TEXT_COLOR', ),
    'Booking Form': ('BACKGROUND_COLOR_BOOKING_FORM', ),
    'Menu Page': ('MANU_PAGE_CONTENT', ),
    'Button': ('BUTTON_BACKGROUND_COLOR', 'BUTTON_HOVER_COLOR', 'BUTTON_TEXT_COLOR', )
}
