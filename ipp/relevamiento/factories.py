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


import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from .models import (Region, Jurisdiccion, Zona, Perfil, Comercio, Rubro,
                    ProductoGenerico, ProductoEnPlanilla, PlanillaModelo, ProductoConMarca,
                    JerarquizacionMarca, PlanillaDeRelevamiento, Lectura, Muestra)


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region


class JurisdiccionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Jurisdiccion


class ZonaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Zona

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'usuario_{}'.format(n))
    email = factory.LazyAttribute(lambda obj: '%s@test.com' % obj.username)
    password = make_password('pass')
    is_active = True

class PerfilFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Perfil

    @factory.post_generation
    def zonas(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for zona in extracted:
                self.zonas.add(zona)

    @factory.post_generation
    def jurisdicciones(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for jurisdiccion in extracted:
                self.jurisdicciones.add(jurisdiccion)

    @factory.post_generation
    def regiones(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for region in extracted:
                self.regiones.add(region)

class ComercioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comercio
    nombre = factory.Sequence(lambda n: 'comercio_{}'.format(n))
    direccion = "irrelevante"
    tipo = "irrelevante"


class RubroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rubro


class ProductoGenericoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductoGenerico

    nombre = factory.Sequence(lambda n: 'usuario_{}'.format(n))
    medida = "irrelevante"

class ProductoEnPlanillaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductoEnPlanilla


class PlanillaModeloFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlanillaModelo


class ProductoConMarcaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductoConMarca


class JerarquizacionMarcaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JerarquizacionMarca


class PlanillaDeRelevamientoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlanillaDeRelevamiento


class LecturaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lectura


class MuestraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Muestra

    @factory.post_generation
    def relevadores(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for relevador in extracted:
                self.relevadores.add(relevador)
