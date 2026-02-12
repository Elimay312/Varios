from __future__ import annotations

import argparse
import os
import sys

from bank_automation.parser import parse_whatsapp_message
from bank_automation.sheets import append_movimiento_if_new, ensure_headers, open_sheet


def main() -> int:
    parser = argparse.ArgumentParser(description="Procesa mensajes de WhatsApp a Google Sheets")
    parser.add_argument("--stdin", action="store_true", help="Leer mensaje desde stdin")
    parser.add_argument("--sheet-id", default=os.getenv("SHEET_ID"), help="Google Sheet ID")
    parser.add_argument("--worksheet", default="movimientos", help="Nombre de la hoja")
    args = parser.parse_args()

    if not args.stdin:
        print("Usa --stdin para pegar el mensaje de WhatsApp")
        return 2

    message = sys.stdin.read().strip()
    mov = parse_whatsapp_message(message)

    if not args.sheet_id:
        print("Movimiento parseado (modo local sin sheet):")
        print(mov)
        return 0

    ws = open_sheet(args.sheet_id, args.worksheet)
    ensure_headers(ws)
    inserted = append_movimiento_if_new(ws, mov)

    if inserted:
        print(f"Guardado movimiento {mov.id_unico}")
    else:
        print(f"Duplicado detectado {mov.id_unico}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
