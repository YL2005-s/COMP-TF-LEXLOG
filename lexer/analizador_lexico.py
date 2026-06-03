import re

# ─── TOKENS DEFINIDOS ────────────────────────────────────────────────────────
COMANDOS = {'DESPACHAR', 'TRANSFERIR', 'VALIDAR', 'CANCELAR', 'CONSULTAR'}
KEYWORDS  = {'DESTINO', 'PRIORIDAD', 'DE', 'HACIA', 'CANTIDAD', 'MOTIVO', 'stock'}
NIVELES   = {'alta', 'media', 'baja'}

# Patrones de tokens
PATRON_IDENTIFICADOR = re.compile(r'^[a-zA-Z]+-\d+$')
PATRON_NUMERO        = re.compile(r'^\d+$')
PATRON_VALOR         = re.compile(r'^[a-zA-Z\u00e0-\u00ff][a-zA-Z0-9\u00e0-\u00ff_-]*$')


def analizar_lexico(instruccion: str) -> dict:
    tokens  = []
    errores = []
    palabras = instruccion.strip().split()

    if not palabras:
        return {'tokens': [], 'errores': ['Instrucción vacía'], 'valido': False}

    for palabra in palabras:
        tipo = clasificar_token(palabra)
        if tipo == 'DESCONOCIDO':
            errores.append(f"Error léxico: token no reconocido → '{palabra}'")
        tokens.append({'valor': palabra, 'tipo': tipo})

    valido = len(errores) == 0
    return {'tokens': tokens, 'errores': errores, 'valido': valido}


def clasificar_token(palabra: str) -> str:
    if palabra in COMANDOS:       return 'COMANDO'
    if palabra in KEYWORDS:       return 'KEYWORD'
    if palabra in NIVELES:        return 'NIVEL'
    if PATRON_NUMERO.match(palabra):        return 'NUMERO'
    if PATRON_IDENTIFICADOR.match(palabra): return 'IDENTIFICADOR'
    if PATRON_VALOR.match(palabra):         return 'VALOR'
    return 'DESCONOCIDO'
