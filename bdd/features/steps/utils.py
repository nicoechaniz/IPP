def seleccionar_primera_opcion(browser, nombre_select):
    select = browser.find_by_name(nombre_select).first
    valor = ''
    for option in select.find_by_tag('option'):
        if not "-----" in option.text:
            valor = option.value
            break
    select.select(valor)
