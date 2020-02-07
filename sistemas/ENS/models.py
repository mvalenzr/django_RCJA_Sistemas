from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from datetime import datetime
from django.contrib.auth.models import User

"""
class Area(models.Model):
    areacodigo = models.CharField(max_length=20)
    areadescripcion = models.CharField(max_length=300)

    def __str__(self):
        # Esta es la variable que identifica los indicadores en el listado del navegador
        return self.areacodigo

    class Meta:
        permissions = (
            # Permission identifier     human-readable permission name
            ('SERVDESK','SERVDESK'), #Gestión del service desk, de la configuración y activos, de incidencias, de eventos y de Problemas
            ('FACTNIVELSERV','FACTNIVELSERV'), #Gestión de la facturación y de los niveles de servicio
            ('PROVISION','PROVISION'), #Gestión de la provisión
            ('CATALOGO','CATALOGO'), #Gestión del catálogo, de la demanda y de la relación con el cliente
            ('INGENIERIA','INGENIERIA'), #Gestión de los sistemas de información, de la disponibilidad y continuidad, de la capacidad, de la homologación y pruebas...
        )
"""

class Sistema(models.Model):
#    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    nombre_sistema = models.CharField(max_length=200)
    descripcion_sistema = models.CharField(max_length=300)
    url_sistema = models.CharField(max_length=300)
#    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """ Esta es la variable que identifica los indicadores en el listado del navegador """
        return self.nombre_sistema
#    def was_published_recently(self):
#        return self.fecha_publicacion >= timezone.now() - datetime.timedelta(days=1)

    class Meta:verbose_name_plural = "Sistemas"


"""
class Indicadorinstancia(models.Model):
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE)
    #indicadorcompletar = models.OneToOneField(Indicadorcompletar, on_delete=models.CASCADE, blank=True, null=True)
    #indicadorcompletar = models.ForeignKey(Indicadorcompletar, on_delete=models.CASCADE, blank=True, null=True)
    descripcion = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True) #solo graba una fecha cuando se crea la instancia
    UNIDADES = [
        ('HORAS', 'HORAS'),
        ('DIAS', 'DIAS'),
        ('MESES', 'MESES'),
        ('PORCENTAJE', 'PORCENTAJE'),
        ('FECHA', 'FECHA'),
        ('NINGUNA', 'NINGUNA'),
    ]
    unidad = models.CharField(
        max_length=20,
        choices=UNIDADES,
        default='NINGUNA',
    )

    valor_objetivo = models.CharField(max_length=200)
    fecha_objetivo = models.DateTimeField('Fecha objetivo')
    valor = models.CharField(max_length=200, null=True, blank=False)
    SELECCION = [
        ('RECHAZADO', 'RECHAZADO'),
        ('PENDIENTE', 'PENDIENTE'),
        ('ACEPTADO', 'ACEPTADO'),
        ('RELLENO', 'RELLENO'),
    ]
    estado = models.CharField(
        max_length=20,
        choices=SELECCION,
        default='PENDIENTE',
    )
    fecha_estado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descripcion

    def muestra_estado(self):
        return self.indicadorcompletar
    muestra_estado.short_description = 'Estado'

    def save(self, *args, **kwargs):
        usuarioactual = get_current_authenticated_user()
        perfil_usuario = User.objects.get(username = usuarioactual.username)

        if perfil_usuario.is_superuser is False :
            #No es superusuario
            if self.valor == '':
                #Si el valor es Null, se lanza una excepción, esto no debería ocurrir mientras en la definición del modelo blank=False
                raise ValidationError('El campo Valor no puede estar vacío.')
            else:
                #Si la instancia se encuentra en valores PENDIENTE o RECHAZADO, automáticamente cambia a estado RELLENO para que lo apruebe o rechace el superusuario
                if self.valor == 'PENDIENTE' or self.valor == 'RECHAZADO':
                    self.fecha_estado = datetime.now()
                    self.estado = 'RELLENO'
                #Para el resto de casos no se
        else :
            #Es superusuario, solo se toma nota de la fecha del cambio de estado
            self.fecha_estado = datetime.now()

        return super(Indicadorinstancia, self).save(*args, **kwargs)


class Indicadorcompletar(models.Model):
    indicadorinstancias = models.ForeignKey(Indicadorinstancia, on_delete=models.SET_NULL, null=True)
    documento = models.FileField(upload_to = 'ENCARGO_RCJA_01/', blank=False)
    comentario = models.CharField(max_length=1000, blank=True)
    fecha_registro = models.DateTimeField() #(auto_now=True, blank=True)
    usuario = models.CharField(max_length=200,  blank=True)

    def __str__(self):
        return str(self.comentario)

    def save(self, *args, **kwargs):

        usuarioactual = get_current_authenticated_user()
        #print(usuarioactual.username)
        self.usuario = usuarioactual.username
        self.fecha_registro=datetime.now()

        self.usuario = usuarioactual.username
        perfil_usuario = User.objects.get(username = self.usuario)

        aux = Indicadorinstancia.objects.get(pk = self.indicadorinstancias_id)
        aux.estado = 'RELLENO'
        aux.save()

        return super(Indicadorcompletar, self).save(*args, **kwargs)
"""