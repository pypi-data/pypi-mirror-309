from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.category import TEMSCategory


class Trial6Category(TEMSCategory):
    class Meta(TEMSCategory.Meta):
        container_path = "/objects/categories/trial6/"
