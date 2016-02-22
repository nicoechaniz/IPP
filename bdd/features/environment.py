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
