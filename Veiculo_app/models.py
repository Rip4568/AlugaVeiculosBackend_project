#Veiculo_app/models.py
from django.core import validators
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from Perfil_app.models import Perfil

class Veiculo(models.Model):
    proprietario = models.ForeignKey(
        Perfil,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Este campo proprietario é um campo O2O, "),
        related_name='veiculos',
        blank=False,
        null=True
    )
    marca = models.CharField(_("Especifique a marca do carro"), max_length=128,
        blank=False,
        null=True,
    )
    modelo = models.CharField(_("Especifique o modelo do carro"), max_length=128,
        blank=True,
        null=True
    )
    ano = models.IntegerField(_("Especifique o ano que o carro foi fabricado"),
        validators=[
        validators.MinLengthValidator(limit_value=4, message=_("Valor minimo especificado para o ano invalido, minimo 4")),
        ],
        null=True,
        blank=False,
    )
    placa = models.CharField(_("Especifique a placa do carro"), max_length=16,
        blank=False,
        null=True,
    )
    cor = models.CharField(_("Especifique a cor do carro"), max_length=16)
    
    alugado = models.BooleanField(_("Este campo tem por objetivo salvar o estado se foi alugado ou não"), 
        default=False,
        blank=True,
        null=True,
    )
    

    class Meta:
        verbose_name = _("veiculo")
        verbose_name_plural = _("veiculos")

    def __str__(self):
        return f'{self.proprietario.nome} - marca: {self.marca} modelo: {self.modelo}'

    def get_absolute_url(self):
        return reverse("veiculo_detail", kwargs={"pk": self.pk})