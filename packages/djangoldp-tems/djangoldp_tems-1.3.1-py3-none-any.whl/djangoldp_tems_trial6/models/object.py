from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_object import baseTEMSObject
from djangoldp_tems.models.provider import TEMSProvider, register_catalog
from djangoldp_tems_trial6.models.keyword import Trial6Keyword


class Trial6Object(baseTEMSObject):
    providers = models.ManyToManyField(
        TEMSProvider, blank=True, related_name="catalog_trial6"
    )
    owners = models.OneToOneField(
        Group,
        related_name="owned_trial6",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    subtitle = models.CharField(max_length=255, blank=True, null=True, default="")
    editor = models.CharField(max_length=255, blank=True, null=True, default="")
    contributors = models.TextField(blank=True, null=True, default="")
    author = models.CharField(max_length=254, blank=True, null=True, default="")
    platform = models.CharField(max_length=254, blank=True, null=True, default="")
    keywords = models.ManyToManyField(Trial6Keyword, blank=True)

    def __str__(self):
        return self.title or self.urlid

    class Meta(baseTEMSObject.Meta):
        container_path = "/objects/trial6/"
        verbose_name = _("TEMS Trial 6 Object")
        verbose_name_plural = _("TEMS Trial 6 Objects")

        serializer_fields = [
            "@id",
            "creation_date",
            "update_date",
            "title",
            "description",
            "copyright",
            "website",
            "licences",
            "images",
            "subtitle",
            "editor",
            "contributors",
            "author",
            "platform",
            "keywords",
            "assets",
            "providers",
            "owners",
        ]
        nested_fields = [
            "licences",
            "assets",
            "images",
            "keywords",
            "providers",
        ]
        rdf_type = ["tems:Object", "tems:ContentObject"]


register_catalog("trial6", Trial6Object)
