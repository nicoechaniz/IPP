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

import datetime

from django.forms import ModelForm, ValidationError, HiddenInput, IntegerField
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.forms import Form, BaseInlineFormSet, EmailField, ChoiceField, ModelChoiceField

import autocomplete_light

from .models import PlanillaDeRelevamiento, JerarquizacionMarca, ProductoConMarca, ProductoGenerico, Muestra, Perfil, Lectura, Zona, Jurisdiccion, Region, Comercio
from .constants import RELEVADOR, COORD_ZONAL, COORD_JURISDICCIONAL, COORD_REGIONAL, COORD_GRAL, MES_CHOICES
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class JerarquizacionMarcaForm(autocomplete_light.ModelForm):
    def __init__(self, *args, **kwargs):
        self.producto_generico_id = kwargs.pop('producto_generico_id', None)
        self.planilla_id = kwargs.pop('planilla_id', None)
        super(JerarquizacionMarcaForm, self).__init__(*args, **kwargs)
        self.fields['producto_con_marca'].label = "Marca"
        if self.producto_generico_id:
            # sólo mostrar opciones relevantes para el producto genérico y que no están siendo usadas
            # en otra jerarquización del mismo producto en esta planilla
            existentes = JerarquizacionMarca.objects.filter(
                producto_con_marca__producto_generico__pk=self.producto_generico_id,
                planilla_de_relevamiento__pk=self.planilla_id)
            self.fields['producto_con_marca'].queryset = ProductoConMarca.objects.filter(
                producto_generico__pk=self.producto_generico_id).exclude(jerarquizaciones__in=existentes)
            self.fields['planilla_de_relevamiento'].widget = HiddenInput()
            self.fields['tipo_marca'].widget = HiddenInput()

    def clean_producto_con_marca(self):
        data = self.cleaned_data.get('producto_con_marca')
        # este caso se da por el uso del auto-complete
        # cuando el usuario envía una cadena de texto en el campo
        if not data:
            raise ValidationError("La marca ingresada es inexistente para este producto.")
        return data

    def clean(self):
        cleaned_data = super(JerarquizacionMarcaForm, self).clean()
        producto_con_marca = cleaned_data.get('producto_con_marca')
        if producto_con_marca:
            #TODO(nicoechaniz): habría que forzar también esta restricción en el modelo?
            producto_generico = producto_con_marca.producto_generico
            tipo_marca = cleaned_data.get('tipo_marca')
            existente = JerarquizacionMarca.objects.filter(
                planilla_de_relevamiento__pk=self.planilla_id,
                producto_con_marca__producto_generico=producto_generico,
                tipo_marca=tipo_marca)
            if existente:
                raise ValidationError("Ya existe una marca %s para ese producto" % tipo_marca)

    class Meta:
        model = JerarquizacionMarca
        exclude = {}
        autocomplete_fields = ('producto_con_marca',)


class ProductoConMarcaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoConMarcaForm, self).__init__(*args, **kwargs)
        self.fields['producto_generico'].widget = HiddenInput()
    
    class Meta:
        model = ProductoConMarca
        exclude = {}

    def clean(self):
        cleaned_data = super(ProductoConMarcaForm, self).clean()
        producto_generico = cleaned_data.get('producto_generico')
        marca = cleaned_data.get('marca')
        existente = ProductoConMarca.objects.filter(producto_generico=producto_generico,
                                                    marca__iexact=marca)
        if existente:
            raise ValidationError("Ya existe la marca %s para ese producto genérico." %\
                                  marca.lower())


class PlanillaDeRelevamientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PlanillaDeRelevamientoForm, self).__init__(*args, **kwargs)
        zonas = self.user.perfil.zonas_permitidas.all()
        self.fields['zona'].queryset = zonas
        comercios = Comercio.objects.filter(zona__in=zonas)
        self.fields['comercio'].queryset = comercios

    def clean_planilla_modelo(self):
        planilla_modelo = self.cleaned_data['planilla_modelo']
        if planilla_modelo.habilitada == True:
            return planilla_modelo
        else:
            raise ValidationError("La planilla modelo seleccionada no está habilitada.")

    def clean_zona(self):
        zona = self.cleaned_data['zona']
        if zona not in self.user.perfil.zonas_permitidas.all():
            raise ValidationError("Zona fuera de sus zonas permitidas.")
        return zona

    def clean_comercio(self):
        comercio = self.cleaned_data['comercio']
        if comercio.zona not in self.user.perfil.zonas_permitidas.all():
            raise ValidationError("Comercio fuera de sus zonas permitidas.")
        return comercio

    def clean(self):
        cleaned_data = super(PlanillaDeRelevamientoForm, self).clean()
        comercio = cleaned_data.get('comercio')
        zona = cleaned_data.get('zona')
        if (comercio and zona) and comercio.zona != zona:
            raise ValidationError("Comercio fuera de la zona seleccionada.")
        
    class Meta:
        model = PlanillaDeRelevamiento
        exclude = {"productos", "habilitada"}


class MuestraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MuestraForm, self).__init__(*args, **kwargs)
        planillas_por_zona = PlanillaDeRelevamiento.objects.filter(
            comercio__zona__in=self.user.perfil.zonas_permitidas.all())
        self.fields['planilla_de_relevamiento'].queryset = planillas_por_zona

        if self.user.perfil.rol == RELEVADOR:
            self.fields['relevadores'].queryset = Perfil.objects.filter(pk=self.user.perfil.pk)
        else:
            perfiles_de_la_zona = Perfil.objects.filter(zonas__in=self.user.perfil.zonas_permitidas.all())
            self.fields['relevadores'].queryset = perfiles_de_la_zona
            
        
    class Meta:
        model = Muestra
        exclude = {"completa", "aprobada", "lecturas"}


class LecturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LecturaForm, self).__init__(*args, **kwargs)
        self.fields['producto_con_marca'].widget = HiddenInput()
        self.fields['muestra'].widget = HiddenInput()

    class Meta:
        model = Lectura
        exclude = {}


class UserFormCreacion(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")


class UserFormEdicion(ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "is_active")


class PerfilInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(PerfilInlineFormSet, self).__init__(*args, **kwargs)
    
    def clean(self):
        super(PerfilInlineFormSet, self).clean()
        hay_datos = False
        for form in self.forms:
            if hasattr(form, "cleaned_data") and form.cleaned_data:
                hay_datos = True
                break
        # Si el form se envía sin completar datos de Perfil, django lo guarda.
        # acá evitamos ese comportamiento y mostramos un error
        if not hay_datos:
            raise ValidationError('La información de perfil está incompleta.')
        else:
            # Si se selecciona Zona sin Jurisdiccion, se la auto-completa aquí
            zonas = form.cleaned_data["zonas"]
            if zonas and not form.cleaned_data["jurisdicciones"]:
                form.cleaned_data["jurisdicciones"] = Jurisdiccion.objects.filter(zonas__in=zonas)

            # Si se selecciona Jurisdicción sin Región, se la auto-completa aquí
            jurisdicciones = form.cleaned_data["jurisdicciones"]
            if jurisdicciones and not form.cleaned_data["regiones"]:
                form.cleaned_data["regiones"] = Region.objects.filter(
                        jurisdicciones__in=jurisdicciones)

            # chequeamos que no haya datos contradictorios
            regiones = form.cleaned_data["regiones"]
            geo_validez = False
            if zonas and jurisdicciones and regiones:
                geo_validez = zonas.filter(jurisdiccion__in=jurisdicciones,
                                           jurisdiccion__region__in=regiones).exists()
            elif jurisdicciones and regiones:
                geo_validez = jurisdicciones.filter(pk__in=jurisdicciones,
                                                    region__in=regiones).exists()
            # si sólo hay regiones, no puede haber incoherencia
            elif regiones:
                geo_validez = True

            if not geo_validez:
                raise ValidationError('La combinación de regiones, jurisdicciones y zonas es inválida.')

PerfilFormSet = inlineformset_factory(User, Perfil, fields="__all__",
                                      can_delete=False, formset=PerfilInlineFormSet)

class VariacionForm(Form):
    # por defecto elije el mes pasado y el mes actual
    anio1 = IntegerField(label="año inico",
                         initial=(datetime.date.today().replace(day=1)-datetime.timedelta(days=1)).year)
    mes1 = ChoiceField(label="mes inico", choices=MES_CHOICES,\
                       initial=(datetime.date.today().replace(day=1)-datetime.timedelta(days=1)).month)
    anio2 = IntegerField(label="año fin", initial=datetime.date.today().year)
    mes2 = ChoiceField(label="mes fin", choices=MES_CHOICES, initial=datetime.date.today().month)
    region = ModelChoiceField(label="región", queryset=Region.objects.all(), required=False)
