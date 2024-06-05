from django.db import models

# Create your models here.

class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    cambio = models.IntegerField(default=0)
    #mano = models.CharField(max_length=100, default="")

class Carta(models.Model):
    numero = models.CharField(max_length=2)
    tipo = models.CharField(max_length=10)
    color = models.CharField(max_length=5)
    jugador = models.ForeignKey('Jugador', related_name='cartas', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.numero} de {self.tipo} ({self.color})"
