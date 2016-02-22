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

