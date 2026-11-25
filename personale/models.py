from django.db import models

class Azienda(models.Model):
    nome = models.CharField(max_length=255)
    partita_iva = models.CharField(max_length=20, blank=True, null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Dipendente(models.Model):
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_assunzione = models.DateField()
    ruolo = models.CharField(max_length=100, default='Dipendente')
    ferie_residue = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)

    def __str__(self):
        return f"{self.nome} {self.cognome} ({self.azienda.nome})"

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Creiamo un "Profilo" che collega l'utente (User) a un'Azienda
class Profilo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.azienda.nome}"

# Questo "ascoltatore" crea automaticamente un Profilo vuoto quando crei un utente
@receiver(post_save, sender=User)
def crea_profilo(sender, instance, created, **kwargs):
    if created:
        # Se non c'è un'azienda, ne creiamo una di default per non far crashare nulla
        azienda_default, _ = Azienda.objects.get_or_create(nome="Azienda Demo")
        Profilo.objects.create(user=instance, azienda=azienda_default)

class RichiestaFerie(models.Model):
    STATO_CHOICES = [
        ('In attesa', 'In attesa'),
        ('Approvata', 'Approvata'),
        ('Rifiutata', 'Rifiutata'),
    ]
    
    dipendente = models.ForeignKey(Dipendente, on_delete=models.CASCADE)
    data_inizio = models.DateField()
    data_fine = models.DateField()
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='In attesa')
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.dipendente.nome} - {self.data_inizio} al {self.data_fine}"