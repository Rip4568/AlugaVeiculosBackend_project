#ContratoAluguel_app/models.py
import asyncio
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators
from django.utils.translation import gettext_lazy as _

from Veiculo_app.models import Veiculo
from Proprietario_app.models import Proprietario
from Perfil_app.models import Perfil

def valida_data_fim(value):
    """
    Validação para garantir que a data de término do contrato seja posterior à data atual.
    """
    if value <= timezone.now():
        raise ValidationError('A data de término do contrato deve ser posterior à data atual.')	

class Contrato(models.Model):
    """
        Modelo de contrato de aluguel de veículo.
    """
    arquivo_contrato = models.FileField(
        _("Este campo arquivo_contrato é um campo para upload de arquivo assinado pelo proprietário do veículo e pela pessoa que alugou o veículo."),
        upload_to='contratos/',
        blank=True,
        null=True
    )
    veiculo = models.ForeignKey(
        _("Este campo veiculo é uma chave estrangeira do veiculo que foi alugado."),
        Veiculo,
        on_delete=models.DO_NOTHING, 
        blank=False, 
        null=True
    )
    alugador = models.ForeignKey(
        _("Este campo alugador é uma chave estrangeira do alugador do veiculo que foi alugado."),
        Perfil,
        on_delete=models.DO_NOTHING, 
        blank=False, 
        null=True
    )
    data_inicio = models.DateField(
        _("Este campo data_inicio é uma data de inicio do contrato de aluguel do veiculo."),
        validators=[validators.MinValueValidator(timezone.now())], 
        default=timezone.now()
    )
    data_fim = models.DateField(
        _("Este campo data_fim é uma data de fim do contrato de aluguel do veiculo."),
        validators=[valida_data_fim],
        default=(timezone.now + timezone.timedelta(days=1)), 
        blank=False, 
        null=True
    )
    valor_diario = models.DecimalField(
        _("Este campo valor_diario é um valor decimal que representa o valor diário do aluguel do veiculo."),
        max_digits=10,
        decimal_places=2, 
        validators=[
            validators.MinValueValidator(0.01), 
            validators.MaxValueValidator(999999.99)
            ], 
        default=1.01, 
        blank=False, 
        null=True
    )
    num_dias_aluguel = models.PositiveSmallIntegerField(
        _("Este campo num_dias_aluguel é um campo inteiro que representa o número de dias que o veiculo foi alugado."), 
        default=1, 
        blank=False, 
        null=True
    )
    dias_atraso = models.PositiveSmallIntegerField(
        _("Este campo dias_atraso é um campo inteiro que representa o número de dias de atraso apos o término do contrato de aluguel do veiculo."),
        default=0,
        blank=True,
        null=True,
    )

    @property
    def valor_total(self):
        return (self.valor_diario * self.num_dias_aluguel) + (self.dias_atraso * self.valor_diario)
    
    def incrementar_dias_de_atraso_pos_vencimento(self):
        self.dias_atraso += 1
        self.save()

    async def enviar_email_alerta(self, assunto:str, mensagem:str, de_email:str, para_email:list[str]):
        await send_mail(assunto, mensagem, de_email, para_email)

    def __str__(self) -> str:
        return f'Contrato de aluguel de {self.veiculo} para {self.alugador}'
