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


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *
# Register your models here.

class ProductoEnPlanillaInline(admin.TabularInline):
    model = ProductoEnPlanilla

class PlanillaModeloAdmin(admin.ModelAdmin):
    inlines = [ProductoEnPlanillaInline,]

class JerarquizacionMarcaAdmin(admin.TabularInline):
    model = JerarquizacionMarca

class PlanillaDeRelevamientoAdmin(admin.ModelAdmin):
    inlines = [JerarquizacionMarcaAdmin]

class LecturaAdmin(admin.TabularInline):
    model = Lectura

class MuestraAdmin(admin.ModelAdmin):
    inlines = [LecturaAdmin]

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
   
class UserAdmin(BaseUserAdmin):
    # Hack feo para colapsar fieldsets de permisos y fechas en el admin de Usuario
    fieldsets = BaseUserAdmin.fieldsets 
    fieldsets[2][1]["classes"] = ["collapse",]
    fieldsets[3][1]["classes"] = ["collapse",]
    
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
       self.inlines = [PerfilInline]
       return super(UserAdmin, self).change_view(*args, **kwargs)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(PlanillaModelo, PlanillaModeloAdmin)
admin.site.register(PlanillaDeRelevamiento, PlanillaDeRelevamientoAdmin)
admin.site.register(Muestra, MuestraAdmin)

for m in [Region, Jurisdiccion, Zona, Comercio, Rubro, ProductoGenerico, ProductoEnPlanilla, ProductoConMarca, JerarquizacionMarca, Lectura]:
    admin.site.register(m)
