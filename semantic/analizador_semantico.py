
# ─── BASE DE DATOS SIMULADA ──────────────────────────────────────────────────
DESTINOS_VALIDOS   = {'Lima', 'Arequipa', 'Trujillo', 'Cusco', 'Piura', 'Chiclayo'}
ALMACENES_VALIDOS  = {'almacen-A', 'almacen-B', 'almacen-C', 'almacen-D'}
PEDIDOS_VALIDOS    = {f'pedido-{str(i).zfill(3)}' for i in range(1, 21)}   # pedido-001..020
LOTES_VALIDOS      = {f'lote-{str(i).zfill(2)}'   for i in range(1, 11)}   # lote-01..10
PRODUCTOS_VALIDOS  = {f'producto-{str(i).zfill(2)}' for i in range(1, 16)} # producto-01..15
MOTIVOS_VALIDOS    = {'dañado', 'extraviado', 'duplicado', 'cancelado', 'devuelto'}


def analizar_semantico(tokens: list) -> dict:
    """
    Verifica que el significado de la instrucción sea lógicamente
    correcto dentro del dominio logístico de la empresa.
    """
    errores = []

    if not tokens:
        return {'errores': ['Sin tokens para analizar'], 'valido': False}

    comando = tokens[0]['valor']
    vals    = [t['valor'] for t in tokens]

    if comando == 'DESPACHAR':
        # DESPACHAR <id> DESTINO <destino> PRIORIDAD <nivel>
        identificador = vals[1]
        destino       = vals[3]

        if identificador not in PEDIDOS_VALIDOS:
            errores.append(
                f"Error semántico: el pedido '{identificador}' "
                f"no existe en el sistema logístico"
            )
        if destino not in DESTINOS_VALIDOS:
            errores.append(
                f"Error semántico: '{destino}' no es un destino "
                f"logístico válido. Válidos: {sorted(DESTINOS_VALIDOS)}"
            )

    elif comando == 'TRANSFERIR':
        # TRANSFERIR <id> DE <origen> HACIA <destino>
        identificador = vals[1]
        origen        = vals[3]
        destino       = vals[5]

        if identificador not in LOTES_VALIDOS:
            errores.append(
                f"Error semántico: el lote '{identificador}' "
                f"no existe en el sistema logístico"
            )
        if origen not in ALMACENES_VALIDOS:
            errores.append(
                f"Error semántico: '{origen}' no es un almacén válido. "
                f"Válidos: {sorted(ALMACENES_VALIDOS)}"
            )
        if destino not in ALMACENES_VALIDOS:
            errores.append(
                f"Error semántico: '{destino}' no es un almacén válido. "
                f"Válidos: {sorted(ALMACENES_VALIDOS)}"
            )
        if origen == destino:
            errores.append(
                f"Error semántico: el origen y destino no pueden "
                f"ser el mismo almacén ('{origen}')"
            )

    elif comando == 'VALIDAR':
        # VALIDAR stock <producto> CANTIDAD <numero>
        producto  = vals[2]
        cantidad  = int(vals[4])

        if producto not in PRODUCTOS_VALIDOS:
            errores.append(
                f"Error semántico: el producto '{producto}' "
                f"no existe en el inventario"
            )
        if cantidad <= 0:
            errores.append(
                f"Error semántico: la cantidad debe ser mayor a 0, "
                f"se recibió {cantidad}"
            )

    elif comando == 'CANCELAR':
        # CANCELAR <id> MOTIVO <motivo>
        identificador = vals[1]
        motivo        = vals[3]

        if identificador not in PEDIDOS_VALIDOS:
            errores.append(
                f"Error semántico: el pedido '{identificador}' "
                f"no existe en el sistema"
            )
        if motivo not in MOTIVOS_VALIDOS:
            errores.append(
                f"Error semántico: '{motivo}' no es un motivo válido. "
                f"Válidos: {sorted(MOTIVOS_VALIDOS)}"
            )

    elif comando == 'CONSULTAR':
        # CONSULTAR <id>
        identificador = vals[1]
        todos = PEDIDOS_VALIDOS | LOTES_VALIDOS | PRODUCTOS_VALIDOS
        if identificador not in todos:
            errores.append(
                f"Error semántico: '{identificador}' "
                f"no existe en ningún registro del sistema"
            )

    valido = len(errores) == 0
    return {'errores': errores, 'valido': valido}
