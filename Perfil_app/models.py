from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from User_app.models import User

class Perfil(models.Model):
    nome = models.CharField(_("Este campo recebe o nome completo do usuario"), max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='perfil')

    class Meta:
        verbose_name = _("perfil")
        verbose_name_plural = _("perfis")

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("perfil_detail", kwargs={"pk": self.pk})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()
