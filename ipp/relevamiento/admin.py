# -*- coding: utf-8 -*-

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
