from django.utils.translation import gettext_lazy as _

from cms.menu_bases import CMSAttachMenu
from menus.menu_pool import menu_pool


class FooterMenu(CMSAttachMenu):
    name = _("Footer Menu")  # give the menu a name this is required.

    def get_nodes(self, request):
        """
        This method is used to build the menu tree.
        """
        nodes = []

        return nodes


menu_pool.register_menu(FooterMenu)
