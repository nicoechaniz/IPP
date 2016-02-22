# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages

from .constants import PERMISO_RELEVADOR, PERMISO_COORD_ZONAL, PERMISO_COORD_JURISDICCIONAL,\
    PERMISO_COORD_REGIONAL, PERMISO_COORD_GRAL

class RequiereRol(UserPassesTestMixin):
    permiso_minimo = None

    def test_func(self):
        if self.permiso_minimo and hasattr(self.request.user, "perfil") and \
           self.request.user.perfil.autorizacion >= self.permiso_minimo:
            return True

    def handle_no_permission(self):
        messages.error(self.request, 'Permisos insuficientes.')
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class RequiereRelevador(RequiereRol):
    permiso_minimo = PERMISO_RELEVADOR

class RequiereCoordZonal(RequiereRol):
    permiso_minimo = PERMISO_COORD_ZONAL

class RequiereCoordJurisdiccional(RequiereRol):
    permiso_minimo = PERMISO_COORD_JURISDICCIONAL

class RequiereCoordRegional(RequiereRol):
    permiso_minimo = PERMISO_COORD_REGIONAL

class RequiereCoordGral(RequiereRol):
    permiso_minimo = PERMISO_COORD_GRAL

