from django.db import models
from django.contrib.auth.models import User

class Programador(models.Model):
    Nombre = models.CharField(max_length=50)
    Pais = models.CharField(max_length=3)
    Fecha_nam = models.DateField()
    Puntuacion = models.PositiveSmallIntegerField()
    email = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + ' - ' + self.user.username