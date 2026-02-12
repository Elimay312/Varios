from __future__ import annotations

from dataclasses import asdict

import gspread

from bank_automation.parser import Movimiento

HEADERS = [
    "fecha",
    "descripcion",
    "referencia_1",
    "monto_entrada",
    "monto_salida",
    "id_unico",
    "estado",
]


def open_sheet(sheet_id: str, worksheet_name: str = "movimientos"):
    gc = gspread.service_account()
    sh = gc.open_by_key(sheet_id)
    return sh.worksheet(worksheet_name)


def ensure_headers(ws) -> None:
    current = ws.row_values(1)
    if current != HEADERS:
        ws.update("A1:G1", [HEADERS])


def get_existing_ids(ws) -> set[str]:
    values = ws.col_values(6)
    # Excluir encabezado
    return set(values[1:]) if len(values) > 1 else set()


def append_movimiento_if_new(ws, mov: Movimiento) -> bool:
    existing = get_existing_ids(ws)
    if mov.id_unico in existing:
        return False

    data = asdict(mov)
    row = [
        data["fecha"],
        data["descripcion"],
        data["referencia_1"],
        data["monto_entrada"],
        data["monto_salida"],
        data["id_unico"],
        "nuevo",
    ]
    ws.append_row(row, value_input_option="USER_ENTERED")
    return True
