# Varios
nel
Base inicial para automatizar revisión de movimientos bancarios con:

- **Python** para procesamiento y reglas.
- **WhatsApp** como fuente de datos de identificación.
- **Google Sheets** como tablero de control.

## Objetivo del flujo

1. Recibir un mensaje de WhatsApp con datos de movimiento.
2. Parsear campos clave: `fecha`, `descripcion`, `referencia_1`, `valor`.
3. Separar automáticamente en:
   - `monto_entrada` (abonos)
   - `monto_salida` (débitos)
4. Generar `id_unico` para detectar duplicados.
5. Guardar en Google Sheets.
6. Ejecutar cada hora (cron, Cloud Run Job o scheduler).

## Estructura

```text
bank_automation/
  parser.py     # Normalización/parseo de mensajes y montos
  sheets.py     # Escritura y deduplicación en Google Sheets
main.py         # Punto de entrada CLI para pruebas rápidas
tests/
  test_parser.py
```

## Formato sugerido del mensaje WhatsApp

Para arrancar rápido, usa este formato simple en texto:

```text
fecha: 2026-02-12
descripcion: Pago qr ruben dario
referencia_1: 0069814846
valor: COP -$7.187.000
```

> También acepta variantes como `COP $70.000`, `70000`, `-70000`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Variables de entorno

```bash
export SHEET_ID="tu_google_sheet_id"
export GOOGLE_APPLICATION_CREDENTIALS="/ruta/service-account.json"
```

## Probar parseo local

```bash
python main.py --stdin
```

Pega el mensaje WhatsApp y cierra con `Ctrl+D`.

## Ejecutar tests

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Próximo paso recomendado

Integrar este parser con un webhook oficial (Twilio WhatsApp o Meta WhatsApp Cloud API) para ingestión automática.
