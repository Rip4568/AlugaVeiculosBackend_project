from django.core import validators
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _


class Proprietario(models.Model):
    nome = models.CharField(_("Nome completo do proprietario"), max_length=50)
    """ o proprietario vai ser uma chave estrangeira de user ou perfil """
    

    class Meta:
        verbose_name = _("proprietario")
        verbose_name_plural = _("proprietarios")
        

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("proprietario_detail", kwargs={"pk": self.pk})
