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


from behave import *
from splinter.browser import Browser
from django.core import management

from ipp.relevamiento.factories import *
from ipp.relevamiento.constants import RELEVADOR, COORD_ZONAL, COORD_JURISDICCIONAL, COORD_REGIONAL, COORD_GRAL

def before_all(context):
    # Unless we tell our test runner otherwise, set our default browser to PhantomJS
    if context.config.browser:
        context.browser = Browser(context.config.browser)
    else:
        context.browser = Browser('phantomjs')
    # si la ventana es pequeña hay elementos que fallan al querer clickearlos
    context.browser.driver.set_window_size(1280, 1024)

def before_scenario(context, scenario):
    management.call_command('flush', verbosity=0, interactive=False)

    # At this stage we can (optionally) mock additional data to setup in the database.
    # For example, if we know that all of our tests require a 'SiteConfig' object,
    # we could create it here.

    region = RegionFactory(nombre="C.A.B.A.")
    jurisdiccion = JurisdiccionFactory(nombre="C.A.B.A.", region=region)
    zona = ZonaFactory(nombre="Comunas 5 y 3", jurisdiccion=jurisdiccion)
    ComercioFactory(zona=zona)

    user_r = UserFactory()
    relevador = PerfilFactory(rol=RELEVADOR, user=user_r, zonas=[zona])
    user_cz = UserFactory()
    coordinador_z = PerfilFactory(rol=COORD_ZONAL, user=user_cz,
                                zonas=[zona],)
    user_cj = UserFactory()
    coordinador_j = PerfilFactory(rol=COORD_JURISDICCIONAL, user=user_cj,
                                jurisdicciones=[jurisdiccion],)
    user_cr = UserFactory()
    coordinador_r = PerfilFactory(rol=COORD_REGIONAL, user=user_cr,
                                regiones=[region],)
    user_cg = UserFactory()
    coordinador_g = PerfilFactory(rol=COORD_GRAL, user=user_cg)

    rubro = RubroFactory(nombre="Almacén")
    planilla_modelo = PlanillaModeloFactory(nombre="Formulario de precios",
                                            habilitada=True)
    contador = 1
    for nombre in ["Azúcar", "Aceite"]:
        producto = ProductoGenericoFactory(nombre=nombre, rubro=rubro)
        ProductoEnPlanillaFactory(producto_generico=producto,
                                  planilla_modelo=planilla_modelo, orden=contador)
        contador +=1
                    
    context.MARCA_POR_DEFECTO = "UnaMarca"
    
def after_all(context):
    context.browser.quit()
    context.browser = None

def after_step(context, step):
    if step.status == "failed":
        # -- SOLUTION: But note that step.exc_info does not exist, yet.
        import ipdb
        ipdb.post_mortem(step.exc_traceback)
