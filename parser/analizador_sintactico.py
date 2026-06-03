
# ─── GRAMÁTICAS ESPERADAS ────────────────────────────────────────────────────
# DESPACHAR  <IDENTIFICADOR> DESTINO <VALOR>       PRIORIDAD <NIVEL>
# TRANSFERIR <IDENTIFICADOR> DE      <VALOR>       HACIA     <VALOR>
# VALIDAR    stock           <IDENTIFICADOR>       CANTIDAD  <NUMERO>
# CANCELAR   <IDENTIFICADOR> MOTIVO  <VALOR>
# CONSULTAR  <IDENTIFICADOR>

GRAMATICAS = {
    'DESPACHAR':  ['COMANDO', 'IDENTIFICADOR', 'KEYWORD', 'VALOR',        'KEYWORD', 'NIVEL'],
    'TRANSFERIR': ['COMANDO', 'IDENTIFICADOR', 'KEYWORD', 'VALOR',        'KEYWORD', 'VALOR'],
    'VALIDAR':    ['COMANDO', 'KEYWORD',        'IDENTIFICADOR',           'KEYWORD', 'NUMERO'],
    'CANCELAR':   ['COMANDO', 'IDENTIFICADOR', 'KEYWORD', 'VALOR'],
    'CONSULTAR':  ['COMANDO', 'IDENTIFICADOR'],
}

KEYWORDS_ESPERADOS = {
    'DESPACHAR':  {2: 'DESTINO',   4: 'PRIORIDAD'},
    'TRANSFERIR': {2: 'DE',        4: 'HACIA'},
    'VALIDAR':    {1: 'stock',     3: 'CANTIDAD'},
    'CANCELAR':   {2: 'MOTIVO'},
}


def analizar_sintactico(tokens: list) -> dict:
    """
    Recibe la lista de tokens del analizador léxico y verifica
    que la estructura sea correcta según la gramática BNF definida.
    """
    errores = []

    if not tokens:
        return {'errores': ['Sin tokens para analizar'], 'valido': False}

    # El primer token debe ser un COMANDO
    primer = tokens[0]
    if primer['tipo'] != 'COMANDO':
        errores.append(
            f"Error sintáctico: se esperaba un COMANDO al inicio, "
            f"se encontró '{primer['valor']}' ({primer['tipo']})"
        )
        return {'errores': errores, 'valido': False}

    comando    = primer['valor']
    gramatica  = GRAMATICAS.get(comando)
    kw_esperados = KEYWORDS_ESPERADOS.get(comando, {})

    if not gramatica:
        errores.append(f"Error sintáctico: comando '{comando}' no tiene gramática definida")
        return {'errores': errores, 'valido': False}

    tipos_tokens = [t['tipo'] for t in tokens]

    # Verificar longitud
    if len(tipos_tokens) != len(gramatica):
        errores.append(
            f"Error sintáctico: se esperaban {len(gramatica)} elementos, "
            f"se encontraron {len(tipos_tokens)}"
        )
        return {'errores': errores, 'valido': False}

    # Verificar tipo de cada posición
    for i, (esperado, token) in enumerate(zip(gramatica, tokens)):
        if token['tipo'] != esperado:
            errores.append(
                f"Error sintáctico en posición {i+1}: "
                f"se esperaba {esperado}, se encontró '{token['valor']}' ({token['tipo']})"
            )

    # Verificar keywords específicos por posición
    for pos, kw in kw_esperados.items():
        if pos < len(tokens) and tokens[pos]['valor'] != kw:
            errores.append(
                f"Error sintáctico en posición {pos+1}: "
                f"se esperaba '{kw}', se encontró '{tokens[pos]['valor']}'"
            )

    valido = len(errores) == 0
    return {'errores': errores, 'valido': valido}
