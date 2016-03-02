# -*- coding: utf-8 -*-

#    IPP, Plataforma web del Índice de Precios Popular
#    Copyright (c) 2016 Nicolás Echániz and contributors.
#
#    This file is part of IPP
#
#    IPP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.




from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime

from .constants import RELEVADOR, COORD_ZONAL, COORD_JURISDICCIONAL, COORD_REGIONAL, COORD_GRAL,\
    PERMISO_RELEVADOR, PERMISO_COORD_ZONAL, PERMISO_COORD_JURISDICCIONAL,\
    PERMISO_COORD_REGIONAL, PERMISO_COORD_GRAL, MES_CHOICES


class Region(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "región"
        verbose_name_plural = "regiones"


class Jurisdiccion(models.Model):
    region = models.ForeignKey(Region, related_name="jurisdicciones")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.region) +" > "+ self.nombre

    class Meta:
        verbose_name = "jurisdicción"
        verbose_name_plural = "jurisdicciones"
        ordering = ['region__pk', 'nombre']
        unique_together = (("region", "nombre"))

class Zona(models.Model):
    jurisdiccion = models.ForeignKey(Jurisdiccion, related_name="zonas")
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return str(self.jurisdiccion) +" > "+ self.nombre

    class Meta:
        ordering = ['jurisdiccion__region__pk', 'jurisdiccion__nombre', 'nombre']
        unique_together = (("jurisdiccion", "nombre"))


class Perfil(models.Model):
    ROLES_CHOICES = (
        (RELEVADOR, RELEVADOR),
        (COORD_ZONAL, COORD_ZONAL),
        (COORD_JURISDICCIONAL, COORD_JURISDICCIONAL),
        (COORD_REGIONAL, COORD_REGIONAL),
        (COORD_GRAL, COORD_GRAL)
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(choices=ROLES_CHOICES, default=RELEVADOR, max_length=40)
    telefono = models.CharField("teléfono", max_length=100, blank=True)
    celular = models.CharField(max_length=100, blank=True)
    enlace = models.URLField(blank=True)
    notas = models.TextField(blank=True)
    regiones = models.ManyToManyField(Region, blank=True)
    jurisdicciones = models.ManyToManyField(Jurisdiccion, blank=True)
    zonas = models.ManyToManyField(Zona, blank=True, related_name="perfiles")

    def __str__(self):
        return self.user.username

    @property
    def autorizacion(self):
        if self.rol == RELEVADOR: return PERMISO_RELEVADOR
        elif self.rol == COORD_ZONAL: return PERMISO_COORD_ZONAL
        elif self.rol == COORD_JURISDICCIONAL: return PERMISO_COORD_JURISDICCIONAL
        elif self.rol == COORD_REGIONAL: return PERMISO_COORD_REGIONAL
        elif self.rol == COORD_GRAL: return PERMISO_COORD_GRAL
        else: return 0

    @property
    def regiones_permitidas(self):
        if self.rol == COORD_REGIONAL:
            return self.regiones
        elif self.rol == COORD_GRAL:
            return Region.objects.all()
        else:
            return Region.objects.none()

    @property
    def jurisdicciones_permitidas(self):
        if self.rol == COORD_JURISDICCIONAL:
            return self.jurisdicciones
        elif self.rol == COORD_REGIONAL:
            return Jurisdiccion.objects.filter(region__in=self.regiones.all())
        elif self.rol == COORD_GRAL:
            return Jurisdiccion.objects.all()
        else:
            return Jurisdiccion.objects.none()

    @property
    def zonas_permitidas(self):
        if self.rol in [RELEVADOR, COORD_ZONAL]:
            return self.zonas
        elif self.rol == COORD_JURISDICCIONAL:
            return Zona.objects.filter(jurisdiccion__in=self.jurisdicciones.all())
        elif self.rol == COORD_REGIONAL:
            return Zona.objects.filter(jurisdiccion__region__in=self.regiones.all())
        elif self.rol == COORD_GRAL:
            return Zona.objects.all()
        else:
            return Zona.objects.none()
        
    class Meta:
        verbose_name_plural = "perfiles"

class Comercio(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField("dirección", max_length=100)
    tipo = models.CharField("tipo de comercio", max_length=100)
    descripcion = models.CharField("descripción", max_length=256, blank=True)
    zona =  models.ForeignKey(Zona, related_name="comercios")

    def __str__(self):
        return self.nombre

class Rubro(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

    
class ProductoGenerico(models.Model):
    rubro = models.ForeignKey(Rubro)
    nombre = models.CharField(max_length=150)
    medida = models.CharField(max_length=20)

    def __str__(self):
        return "%s > %s (%s)" % (self.rubro, self.nombre, self.medida)
    
    class Meta:
        verbose_name_plural="productos genericos"


class ProductoEnPlanilla(models.Model):
    producto_generico = models.ForeignKey(ProductoGenerico)
    planilla_modelo = models.ForeignKey("PlanillaModelo")
    orden = models.IntegerField()
    def __str__(self):
        return str(self.producto_generico)

    class Meta:
        unique_together = (("planilla_modelo", "orden"), ("planilla_modelo", "producto_generico"))


class PlanillaModelo(models.Model):
    """Planilla que establece qué productos se relevarán en todo el sistema"""
    nombre = models.CharField(max_length=100)
    productos = models.ManyToManyField(ProductoGenerico,
                                       through=ProductoEnPlanilla, blank=True)
    habilitada = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural="planillas modelo"


class ProductoConMarca(models.Model):
    producto_generico = models.ForeignKey(ProductoGenerico)
    marca = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "%s %s" %\
            (str(self.producto_generico), self.marca)

    class Meta:
        verbose_name="producto"
        verbose_name_plural="productos"
        unique_together = (("producto_generico", "marca"),)

class JerarquizacionMarca(models.Model):
    MARCA_CHOICES = (
        ("premium", "premium"),
        ("media", "media"),
        ("economica", "económica")
    )
    planilla_de_relevamiento = models.ForeignKey("PlanillaDeRelevamiento")
    producto_con_marca = models.ForeignKey(ProductoConMarca, related_name="jerarquizaciones", verbose_name="producto")
    tipo_marca = models.CharField(choices=MARCA_CHOICES, max_length=15)
    def __str__(self):
        return "%s (marca %s)" %\
            (str(self.producto_con_marca), self.tipo_marca)

    class Meta:
        unique_together = (("planilla_de_relevamiento", "producto_con_marca"),)


class PlanillaDeRelevamiento(models.Model):
    """Basada en una Planilla Modelo, establece qué marcas se relevarán para un comercio específico"""
    planilla_modelo = models.ForeignKey(PlanillaModelo)
    zona = models.ForeignKey(Zona, related_name="planillas_de_relevamiento")
    comercio = models.ForeignKey(Comercio, related_name="planillas_de_relevamiento")
    productos = models.ManyToManyField(ProductoConMarca,
                                       through=JerarquizacionMarca, blank=True)
    habilitada = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % \
            (str(self.comercio), str(self.zona))

    class Meta:
        unique_together = (("planilla_modelo", "zona", "comercio"),)
        verbose_name_plural = "planillas de relevamiento"
        ordering = ['planilla_modelo__nombre', 'zona']


class Lectura(models.Model):
    producto_con_marca = models.ForeignKey(ProductoConMarca, verbose_name="producto")
    precio = models.FloatField()
    fecha = models.DateField(default=datetime.now)
    muestra = models.ForeignKey('Muestra', related_name="lecturas")
#    relevador = models.ForeignKey(Perfil)

    def __str__(self):
        return "%s $%s (%s)" % \
            (str(self.producto_con_marca), str(self.precio), str(self.fecha))

    class Meta:
        unique_together = (("producto_con_marca", "muestra"),)


class Muestra(models.Model):
    """Muestra de lecturas quincenales para un comercio"""
    planilla_de_relevamiento = models.ForeignKey(PlanillaDeRelevamiento, related_name="muestras")
    anio = models.IntegerField("año")
    mes = models.IntegerField(choices=MES_CHOICES)
    quincena = models.IntegerField(choices=((1, "primera"),(2, "segunda")))
    relevadores = models.ManyToManyField(Perfil, blank=True)
    completa = models.BooleanField(default=False)
    aprobada = models.BooleanField(default=False)
    
    def __str__(self):
        nombre = "%s (%s/%s, quincena %s)" %\
                 (str(self.planilla_de_relevamiento), self.mes, self.anio, self.quincena)
        return nombre

    class Meta:
        unique_together = (("planilla_de_relevamiento", "anio", "mes", "quincena"),)
        ordering = ['-anio', '-mes', '-quincena']
