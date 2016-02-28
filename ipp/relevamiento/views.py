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


from collections import OrderedDict

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.db.models import Q, F, Avg, Max, Min, Count
from django.utils.text import slugify

import unicodecsv as csv

from .constants import PERMISO_RELEVADOR, PERMISO_COORD_ZONAL, PERMISO_COORD_JURISDICCIONAL,\
    PERMISO_COORD_REGIONAL, PERMISO_COORD_GRAL, RELEVADOR, COORD_ZONAL, COORD_JURISDICCIONAL,\
    COORD_REGIONAL, COORD_GRAL
from .forms import PlanillaDeRelevamientoForm, JerarquizacionMarcaForm, ProductoConMarcaForm,\
    MuestraForm, LecturaForm, UserFormCreacion, UserFormEdicion, PerfilFormSet
from .models import PlanillaModelo, PlanillaDeRelevamiento, JerarquizacionMarca, ProductoGenerico,\
    ProductoConMarca, Lectura, Comercio, Perfil, Muestra, PlanillaDeRelevamiento, JerarquizacionMarca,\
    Zona, Comercio, Jurisdiccion, Region
from .perms import RequiereCoordZonal, RequiereCoordJurisdiccional, RequiereCoordRegional


def crear_planilla_de_relevamiento(request):
    user=request.user
    if hasattr(user, "perfil") and \
       user.perfil.autorizacion >= PERMISO_COORD_ZONAL:
        if request.method == "POST":
            form = PlanillaDeRelevamientoForm(request.POST, user=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'La planilla de relevamiento fue creada con éxito.')
                return render(request, 'relevamiento/mensaje.html')
            else:
                return render(request, 'relevamiento/crear_planilla_de_relevamiento.html',
                              {"form": form})
        else:
                planillas_modelo = PlanillaModelo.objects.all()
                initial = {}
                if len(planillas_modelo) == 1:
                    planilla_modelo = planillas_modelo[0]
                    initial = {"planilla_modelo": planilla_modelo}
                form = PlanillaDeRelevamientoForm(initial=initial, user=user)
                return render(request, 'relevamiento/crear_planilla_de_relevamiento.html',
                              {"form": form})
    else:
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')

def json_opciones_zona(request):
# tiene que devolver las opciones de zona habilitadas para el usuario
    pass

def json_opciones_comercio(request):
# tiene que devolver las opciones de comercios para la zona elegida
    pass

def seleccionar_planilla_de_relevamiento(request):
    user = request.user
    if hasattr(request.user, "perfil") and \
       request.user.perfil.autorizacion >= PERMISO_RELEVADOR:
        if request.user.perfil.rol == RELEVADOR:
            seleccion = PlanillaDeRelevamiento.objects.filter(zona__in=user.perfil.zonas_permitidas.all())
        else:
            seleccion = PlanillaDeRelevamiento.objects.filter(zona__in=user.perfil.zonas_permitidas.all())
        if not seleccion:
            messages.error(request, 'No existen planillas de relevamiento para sus zonas.')
            return render(request, 'relevamiento/mensaje.html')
        return render(request, 'relevamiento/seleccionar_planilla_de_relevamiento.html',
                      {"seleccion": seleccion})

def completar_planilla_de_relevamiento(request, planilla_id):
    if not (hasattr(request.user, "perfil") and \
            request.user.perfil.autorizacion >= PERMISO_RELEVADOR):
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')
    try:
        planilla_de_relevamiento = PlanillaDeRelevamiento.objects.get(pk=planilla_id)
    except PlanillaDeRelevamiento.DoesNotExist:
        raise Http404("La planilla de relevamiento requerida es inexistente.")

    contexto = {"planilla": planilla_de_relevamiento, "comercio": planilla_de_relevamiento.comercio,
                "zona": planilla_de_relevamiento.zona, "autorizacion": request.user.perfil.autorizacion }

    planilla_modelo = planilla_de_relevamiento.planilla_modelo

    productos_con_marca = []
    for producto in planilla_modelo.productos.all():
        marcas = OrderedDict([("economica", ""), ("media", ""), ("premium", "")])
        for producto_con_marca in \
            planilla_de_relevamiento.productos.filter(
                producto_generico=producto):

            jerarquizacion = JerarquizacionMarca.objects.get(
                planilla_de_relevamiento=planilla_de_relevamiento,
                producto_con_marca=producto_con_marca)

            marca = producto_con_marca.marca
            tipo_marca = jerarquizacion.tipo_marca

            marcas[tipo_marca] = marca

        productos_con_marca.append({"producto": producto, "marcas": marcas})

    contexto["datos"] = productos_con_marca
    return render(request, 'relevamiento/planilla_de_relevamiento.html', contexto)


def habilitar_planilla_de_relevamiento(request, planilla_id):
    if not (hasattr(request.user, "perfil") and \
            request.user.perfil.autorizacion >= PERMISO_COORD_ZONAL):
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')
    try:
        planilla_de_relevamiento = PlanillaDeRelevamiento.objects.get(pk=planilla_id)
    except PlanillaDeRelevamiento.DoesNotExist:
        raise Http404("La planilla de relevamiento requerida es inexistente.")

    planilla_de_relevamiento.habilitada = True
    planilla_de_relevamiento.save()
    messages.success(request, 'La planilla de relevamiento fue habilitada.')
    return render(request, 'relevamiento/mensaje.html')

def deshabilitar_planilla_de_relevamiento(request, planilla_id):
    if not (hasattr(request.user, "perfil") and \
            request.user.perfil.autorizacion >= PERMISO_COORD_ZONAL):
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')
    try:
        planilla_de_relevamiento = PlanillaDeRelevamiento.objects.get(pk=planilla_id)
    except PlanillaDeRelevamiento.DoesNotExist:
        raise Http404("La planilla de relevamiento requerida es inexistente.")

    planilla_de_relevamiento.habilitada = False
    planilla_de_relevamiento.save()
    messages.success(request, 'La planilla de relevamiento fue deshabilitada.')
    return render(request, 'relevamiento/mensaje.html')


def establecer_marca(request, planilla_id, tipo_marca, producto_id):
    user=request.user
    if hasattr(user, "perfil") and \
       user.perfil.autorizacion >= PERMISO_RELEVADOR:
        producto = ProductoGenerico.objects.get(pk=producto_id)
        if request.method == "POST":
            form = JerarquizacionMarcaForm(request.POST,
                                           producto_generico_id=producto_id, planilla_id=planilla_id)
            if form.is_valid():
                form.save()
                return redirect(reverse("relevamiento:completar_planilla_de_relevamiento",
                                        kwargs={"planilla_id": planilla_id}))
            else:
                return render(request, 'relevamiento/establecer_jerarquizacion_marca.html',
                              {"form": form, "producto": producto})
        else:
            planilla_de_relevamiento = PlanillaDeRelevamiento.objects.get(pk=planilla_id)
            initial = {"planilla_de_relevamiento": planilla_de_relevamiento, "tipo_marca": tipo_marca}
            form = JerarquizacionMarcaForm(initial=initial, producto_generico_id=producto_id,
                                           planilla_id=planilla_id)
            return render(request, 'relevamiento/establecer_jerarquizacion_marca.html',
                          {"form": form, "producto": producto})
    else:
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')


def nueva_marca(request, producto_id=None):
    user=request.user
    if hasattr(user, "perfil") and \
       user.perfil.autorizacion >= PERMISO_RELEVADOR:
        producto_generico = ProductoGenerico.objects.get(pk=producto_id)
        if request.method == "POST":
            form = ProductoConMarcaForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, 'Marca agregada con éxito.')
                return render(request, 'relevamiento/mensaje_modal.html',
                )
            else:
                return render(request, 'relevamiento/nueva_marca.html',
                              {"form": form, "producto_generico": producto_generico})
        else:
            initial = {"producto_generico": producto_generico}
            form = ProductoConMarcaForm(initial=initial)
            return render(request, 'relevamiento/nueva_marca.html',
                          {"form": form, "producto_generico": producto_generico})
    else:
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')
    

def remover_marca(request, planilla_id, tipo_marca, producto_id):
    user=request.user
    if hasattr(user, "perfil") and \
       user.perfil.autorizacion >= PERMISO_RELEVADOR:
        try:
            jerarquizacion_marca = JerarquizacionMarca.objects.get(
                planilla_de_relevamiento__pk=planilla_id, tipo_marca=tipo_marca,
                producto_con_marca__producto_generico__pk=producto_id)
        except JerarquizacionMarca.DoesNotExist:
            raise Http404("La jerarquización requerida es inexistente.")

        jerarquizacion_marca.delete()
        return redirect(reverse("relevamiento:completar_planilla_de_relevamiento",
                                kwargs={"planilla_id": planilla_id}))


def seleccionar_muestra(request):
    user = request.user
    if hasattr(request.user, "perfil") and \
       request.user.perfil.autorizacion >= PERMISO_RELEVADOR:
        seleccion = Muestra.objects.filter(
            planilla_de_relevamiento__zona__in=user.perfil.zonas_permitidas.all(),
            planilla_de_relevamiento__habilitada=True, aprobada=False)
        if request.method == "POST":
            form = MuestraForm(request.POST, user=user)
            if form.is_valid():
                form.save()
        else:
            form = MuestraForm(user=user)
        return render(request, 'relevamiento/seleccionar_muestra.html',
                      {"seleccion": seleccion, "form": form})


def editar_muestra(request, muestra_id):
    try:
        muestra = Muestra.objects.get(pk=muestra_id)
    except Muestra.DoesNotExist:
        raise Http404("La muestra requerida es inexistente.")

    contexto = {"muestra": muestra, "mes": muestra.mes, "anio": muestra.anio,
                "quincena": muestra.quincena, "zona": muestra.planilla_de_relevamiento.zona,
                "comercio": muestra.planilla_de_relevamiento.comercio,
                "relevadores": muestra.relevadores.all(),
                "autorizacion": request.user.perfil.autorizacion }

    planilla_modelo = muestra.planilla_de_relevamiento.planilla_modelo
    planilla_de_relevamiento = muestra.planilla_de_relevamiento
    datos = []
    contexto["nombre_planilla"] = planilla_modelo.nombre
    for producto_generico in planilla_modelo.productos.all():
        lecturas = OrderedDict([("economica", {}), ("media", {}), ("premium", {})])        
        for tipo_marca in lecturas.keys():
            try:
                producto_con_marca = planilla_de_relevamiento.productos.get(
                    producto_generico=producto_generico, jerarquizaciones__tipo_marca=tipo_marca)
            except:
                producto_con_marca = None
                
            if producto_con_marca:
                marca = producto_con_marca.marca
                lecturas[tipo_marca]["producto_con_marca"] = producto_con_marca
                try:
                    lectura = muestra.lecturas.get(producto_con_marca=producto_con_marca)
                except:
                    lectura = None
                if lectura:
                    lecturas[tipo_marca]["precio"] = lectura.precio
                    lecturas[tipo_marca]["pk"] = lectura.pk

        datos.append({"producto_generico": producto_generico, "lecturas": lecturas})

    contexto["datos"] = datos
    return render(request, 'relevamiento/editar_muestra.html', contexto)


def crear_lectura(request, lectura_id=None, muestra_id=None, producto_id=None):
    user=request.user
    if hasattr(user, "perfil") and \
       user.perfil.autorizacion >= PERMISO_RELEVADOR:
        if request.method == "POST":
            form = LecturaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse("relevamiento:editar_muestra",
                                        kwargs={"muestra_id": muestra_id}))

            else:
                return render(request, 'relevamiento/crear_lectura.html',
                              {"form": form, "muestra_id": muestra_id, "producto_id": producto_id})
        else:
            try:
                muestra = Muestra.objects.get(pk=muestra_id)
            except Muestra.DoesNotExist:
                raise Http404("La muestra requerida es inexistente.")

            try:
                producto_con_marca = ProductoConMarca.objects.get(pk=producto_id)
            except ProductoConMarca.DoesNotExist:
                raise Http404("El producto requerido es inexistente.")
            
            initial = {"muestra": muestra, "producto_con_marca": producto_con_marca}
            form = LecturaForm(initial=initial)
            return render(request, 'relevamiento/crear_lectura.html',
                              {"form": form, "muestra_id": muestra_id, "producto_id": producto_id})
    else:
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')
    

def editar_lectura(request, lectura_id):
    user=request.user
    if hasattr(user, "perfil") and \
       user.perfil.autorizacion >= PERMISO_RELEVADOR:
        try:
            lectura = Lectura.objects.get(pk=lectura_id)
        except Lectura.DoesNotExist:
            raise Http404("La lectura requerida es inexistente.")
        
        if request.method == "POST":
            form = LecturaForm(request.POST, instance=lectura)
            if form.is_valid():
                form.save()
                return redirect(reverse("relevamiento:editar_muestra",
                                        kwargs={"muestra_id": lectura.muestra.pk}))
            else:
                return render(request, 'relevamiento/editar_lectura.html',
                              {"form": form, "lectura_id": lectura.pk})
        else:
            form = LecturaForm(instance=lectura)
            return render(request, 'relevamiento/editar_lectura.html',
                              {"form": form, "lectura_id": lectura.pk})
    else:
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')

class SeleccionarComercio(RequiereCoordZonal, ListView):
    model = Comercio
    template_name = "relevamiento/seleccionar_comercio.html"
    def get_queryset(self):
        qs = super(SeleccionarComercio, self).get_queryset()
        return qs.filter(zona__in=self.request.user.perfil.zonas_permitidas.all())

class ComercioBase(RequiereCoordZonal):
    model = Comercio
    success_message = "Comercio guardado con éxito"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(ComercioBase, self).get_context_data(**kwargs)
        context['form'].fields['zona'].queryset = self.request.user.perfil.zonas_permitidas.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(ComercioBase, self).form_valid(form)  

class CrearComercio(ComercioBase, CreateView):
    template_name = "relevamiento/crear_comercio.html"
    success_url = "/"
    success_message = "Comercio creado con éxito."


class EditarComercio(ComercioBase, UpdateView):
    template_name = "relevamiento/crear_comercio.html"
    success_url = "/"
    success_message = "Comercio actualizado con éxito."

class SeleccionarZona(RequiereCoordJurisdiccional, ListView):
    model = Zona
    template_name = "relevamiento/seleccionar_zona.html"

    def get_queryset(self):
        return self.request.user.perfil.zonas_permitidas.all()

class ZonaBase(RequiereCoordJurisdiccional):
    model = Zona
    success_message = "Zona guardada con éxito"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(ZonaBase, self).get_context_data(**kwargs)
        jurisdicciones_permitidas = self.request.user.perfil.jurisdicciones_permitidas.all()
        context['form'].fields['jurisdiccion'].queryset = jurisdicciones_permitidas
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(ZonaBase, self).form_valid(form)  


class CrearZona(ZonaBase, CreateView):
    template_name = "relevamiento/crear_zona.html"
    success_url = "/"
    success_message = "Zona creada con éxito."


class EditarZona(ZonaBase, UpdateView):
    template_name = "relevamiento/crear_zona.html"
    success_url = "/"
    success_message = "Zona actualizada con éxito."


class SeleccionarJurisdiccion(RequiereCoordRegional, ListView):
    model = Jurisdiccion
    template_name = "relevamiento/seleccionar_jurisdiccion.html"

    def get_queryset(self):
#        qs = super(SeleccionarJurisdiccion, self).get_queryset()
        qs = self.request.user.perfil.jurisdicciones_permitidas.all()
        return qs

class JurisdiccionBase(RequiereCoordRegional):
    model = Jurisdiccion
    success_message = "Jurisdicción guardada con éxito"
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(JurisdiccionBase, self).get_context_data(**kwargs)
        context['form'].fields['region'].queryset = Region.objects.filter(
            pk__in=self.request.user.perfil.regiones_permitidas.all())
        return context

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(JurisdiccionBase, self).form_valid(form)  

class CrearJurisdiccion(JurisdiccionBase, CreateView):
    template_name = "relevamiento/crear_jurisdiccion.html"
    success_url = "/"
    success_message = "Jurisdiccion creada con éxito."


class EditarJurisdiccion(JurisdiccionBase, UpdateView):
    template_name = "relevamiento/crear_jurisdiccion.html"
    success_url = "/"
    success_message = "Jurisdiccion actualizada con éxito."


class UserBase(RequiereCoordZonal):
    template_name = 'relevamiento/crear_user.html'
    model = User

    def get(self, request, *args, **kwargs):
        if not self.kwargs.get("pk", None):
            self.object = None
        else:
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if self.object:
            perfil_form = PerfilFormSet(instance=self.object)
        else:
            perfil_form = PerfilFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  perfil_form=perfil_form))

    def post(self, request, *args, **kwargs):
        if not self.kwargs.get("pk", None):
            self.object = None
            perfil_form = PerfilFormSet(self.request.POST)
        else:
            self.object = self.get_object()
            perfil_form = PerfilFormSet(self.request.POST, instance=self.object)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid() and perfil_form.is_valid():
            return self.form_valid(form, perfil_form)
        else:
            return self.form_invalid(form, perfil_form)

    def form_valid(self, form, perfil_form):
        self.object = form.save()
        perfil_form.instance = self.object
        perfil_form.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, perfil_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  perfil_form=perfil_form))

    def get_context_data(self, **kwargs):
        context = super(UserBase, self).get_context_data(**kwargs)
        perfil = self.request.user.perfil
        zonas_permitidas =  perfil.zonas_permitidas.all()
        perfil_form = context['perfil_form'].forms[0]
        perfil_form.fields['zonas'].queryset = zonas_permitidas
        jurisdicciones_permitidas =  perfil.jurisdicciones_permitidas.all()
        perfil_form.fields['jurisdicciones'].queryset = jurisdicciones_permitidas
        regiones_permitidas =  perfil.regiones_permitidas.all()
        perfil_form.fields['regiones'].queryset = regiones_permitidas

        roles_permitidos = perfil_form.fields['rol'].choices
        if perfil.rol == COORD_ZONAL:
            roles_permitidos = [(RELEVADOR, RELEVADOR),]
        elif perfil.rol == COORD_JURISDICCIONAL:
            roles_permitidos = [(RELEVADOR, RELEVADOR), (COORD_ZONAL, COORD_ZONAL)]
        elif perfil.rol == COORD_REGIONAL:
            roles_permitidos = [(RELEVADOR, RELEVADOR), (COORD_ZONAL, COORD_ZONAL),
                                (COORD_JURISDICCIONAL, COORD_JURISDICCIONAL)]
        elif perfil.rol == COORD_GRAL:
            roles_permitidos = perfil_form.fields['rol'].choices
        else:
            roles_permitidos = []
        if roles_permitidos != perfil_form.fields['rol'].choices:
            context['perfil_form'].forms[0].fields['rol'].choices = roles_permitidos
        return context

class CrearUser(UserBase, CreateView):
    template_name = 'relevamiento/crear_user.html'
    success_url = '/'
    success_message = "Usuario creado con éxito."
    form_class = UserFormCreacion

class EditarUser(UserBase, UpdateView):
    template_name = 'relevamiento/crear_user.html'
    success_url = '/'
    success_message = "Usuario actualizado con éxito."
    form_class = UserFormEdicion

class SeleccionarUser(RequiereCoordZonal, ListView):
    model = User
    template_name = "relevamiento/seleccionar_user.html"

    def get_queryset(self):
        # mostrar los users que pertenecen a zonas, jurisdicciones y regiones permitidas
        qs = super(SeleccionarUser, self).get_queryset()
        perfil = self.request.user.perfil
        qs = qs.filter(Q(perfil__zonas__in=perfil.zonas_permitidas.all()) |
                       Q(perfil__jurisdicciones__in=perfil.jurisdicciones_permitidas.all()) |
                       Q(perfil__regiones__in=perfil.regiones_permitidas.all())).distinct()
        if perfil.autorizacion < PERMISO_COORD_GRAL:
            if perfil.rol == COORD_REGIONAL:
                qs = qs.filter(perfil__rol__in=[COORD_JURISDICCIONAL, COORD_ZONAL, RELEVADOR])
            elif perfil.rol == COORD_JURISDICCIONAL:
                qs = qs.filter(perfil__rol__in=[COORD_ZONAL, RELEVADOR])
            elif perfil.rol == COORD_ZONAL:
                qs = qs.filter(perfil__rol__in=[RELEVADOR])
        return qs

def descargar_datos(request):
    if not (hasattr(request.user, "perfil") and \
            request.user.perfil.autorizacion >= PERMISO_COORD_ZONAL):
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')

    regiones = Region.objects.all()
    muestras = Muestra.objects.all()\
                              .values("anio", "mes", "quincena")\
                              .annotate(region=F("planilla_de_relevamiento__zona__jurisdiccion__region__nombre"))\
                              .annotate(region_id=F("planilla_de_relevamiento__zona__jurisdiccion__region__id"))\
                              .annotate(cantidad=Count("id")).order_by("-anio", "-mes", "-quincena", "region")
    muestras_pais = Muestra.objects.all().values("anio", "mes", "quincena")\
                                         .annotate(cantidad=Count("id")).order_by("-anio", "-mes", "-quincena")

    return render(request, 'relevamiento/descargar_datos.html',
                  {"regiones": regiones, "muestras": muestras, "muestras_pais": muestras_pais})


def _agregado_por_comercio(request, anio, mes, quincena, region_id, funcion, prefijo):
    if not (hasattr(request.user, "perfil") and \
            request.user.perfil.autorizacion >= PERMISO_COORD_ZONAL):
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')

    muestras = Muestra.objects.filter(anio=anio, mes=mes, quincena=quincena)
    lecturas = Lectura.objects.filter(muestra__in=muestras, precio__gt=0)
    if region_id:
        lecturas = lecturas.filter(
            muestra__planilla_de_relevamiento__zona__jurisdiccion__region__pk=region_id)

    lecturas = lecturas.annotate(orden=F("producto_con_marca__producto_generico__id"))\
                       .annotate(producto=F("producto_con_marca__producto_generico__nombre"))\
                       .annotate(comercio=F('muestra__planilla_de_relevamiento__comercio__nombre'))\
                       .values('comercio', 'producto')\
                       .annotate(valor=funcion('precio'))\
                       .order_by('orden', 'comercio')

    comercios = Comercio.objects.filter(planillas_de_relevamiento__muestras__in=muestras).values("nombre")
    lecturas_por_comercio = OrderedDict()
    encabezado = ["Producto"]

    for lectura in lecturas:
        if lectura['comercio'] not in encabezado:
            encabezado.append(lectura['comercio'])
        lecturas_por_comercio.setdefault(lectura['producto'], {}).update(
            {lectura['comercio']: lectura['valor']})

    nombre_archivo = [prefijo, anio, mes.zfill(2), quincena.zfill(2)]
    if region_id:
        region = Region.objects.get(pk=region_id)
        nombre_archivo.append("_%s" % slugify(region.nombre))
    nombre_archivo.append(".csv")
    nombre_archivo = "".join(nombre_archivo)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s;' % nombre_archivo
    response['Cache-Control'] = 'no-cache'

    writer = csv.DictWriter(response, fieldnames=encabezado)
    writer.writeheader()
    for producto, lecturas_dict in lecturas_por_comercio.items():
        row = {"Producto": producto}
        row.update(lecturas_dict)
        writer.writerow(row)
        
    return response


def promedios_por_comercio(request, anio, mes, quincena, region_id=None):
    return _agregado_por_comercio(request, anio, mes, quincena, region_id, Avg, "promedio_")

def maximos_por_comercio(request, anio, mes, quincena, region_id=None):
    return _agregado_por_comercio(request, anio, mes, quincena, region_id, Max, "maximos_")

def minimos_por_comercio(request, anio, mes, quincena, region_id=None):
    return _agregado_por_comercio(request, anio, mes, quincena, region_id, Min, "minimos_")


def aprobar_muestra(request, muestra_id):
    if not (hasattr(request.user, "perfil") and \
            request.user.perfil.autorizacion >= PERMISO_COORD_ZONAL):
        messages.error(request, 'Permisos insuficientes.')
        return render(request, 'relevamiento/mensaje.html')
    try:
        muestra = Muestra.objects.get(pk=muestra_id)
    except Muestra.DoesNotExist:
        raise Http404("La muestra requerida es inexistente.")

    muestra.aprobada = True
    muestra.save()
    messages.success(request, 'La muestra fue aprobada.')
    return redirect(reverse("relevamiento:seleccionar_muestra"))
