from django.utils.translation import gettext_lazy as _

from djangoldp_tems.models.__base_named_model import baseTEMSNamedModel


class Trial8Compatibility(baseTEMSNamedModel):
    class Meta(baseTEMSNamedModel.Meta):
        container_path = "/objects/compatibilities/trial8/"
        verbose_name = _("TEMS Compatibility")
        verbose_name_plural = _("TEMS Compatibilities")
        rdf_type = "tems:Compatibility"
