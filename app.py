import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify
from lexer.analizador_lexico     import analizar_lexico
from parser.analizador_sintactico import analizar_sintactico
from semantic.analizador_semantico import analizar_semantico

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/procesar', methods=['POST'])
def procesar():
    data        = request.get_json()
    instruccion = data.get('instruccion', '').strip()

    if not instruccion:
        return jsonify({'error': 'Instrucción vacía'}), 400

    resultado = {
        'instruccion': instruccion,
        'fases': {}
    }

    # ── FASE 1: ANÁLISIS LÉXICO ──────────────────────────────
    lexico = analizar_lexico(instruccion)
    resultado['fases']['lexico'] = {
        'tokens':  lexico['tokens'],
        'errores': lexico['errores'],
        'valido':  lexico['valido']
    }

    # Si hay errores léxicos, no continuar
    if not lexico['valido']:
        resultado['valido']  = False
        resultado['fase_fallo'] = 'léxico'
        return jsonify(resultado)

    # ── FASE 2: ANÁLISIS SINTÁCTICO ──────────────────────────
    sintactico = analizar_sintactico(lexico['tokens'])
    resultado['fases']['sintactico'] = {
        'errores': sintactico['errores'],
        'valido':  sintactico['valido']
    }

    if not sintactico['valido']:
        resultado['valido']  = False
        resultado['fase_fallo'] = 'sintáctico'
        return jsonify(resultado)

    # ── FASE 3: ANÁLISIS SEMÁNTICO ───────────────────────────
    semantico = analizar_semantico(lexico['tokens'])
    resultado['fases']['semantico'] = {
        'errores': semantico['errores'],
        'valido':  semantico['valido']
    }

    if not semantico['valido']:
        resultado['valido']  = False
        resultado['fase_fallo'] = 'semántico'
        return jsonify(resultado)

    # ── INSTRUCCIÓN VÁLIDA ───────────────────────────────────
    resultado['valido']  = True
    resultado['mensaje'] = '✅ Instrucción válida. Procesada correctamente.'
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
