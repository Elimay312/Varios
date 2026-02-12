from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Movimiento:
    fecha: str
    descripcion: str
    referencia_1: str
    valor_original: int
    monto_entrada: int
    monto_salida: int
    id_unico: str


def parse_amount_cop(raw: str) -> int:
    """Convierte formatos COP a entero con signo.

    Ejemplos válidos:
    - COP $70.000
    - COP -$7.187.000
    - 70000
    - -70000
    """
    text = raw.strip().upper().replace("COP", "").replace(" ", "")
    negative = "-" in text
    normalized = re.sub(r"[^0-9]", "", text)
    if not normalized:
        raise ValueError(f"No se pudo parsear valor: {raw}")

    amount = int(normalized)
    return -amount if negative else amount


def normalize_date(raw: str) -> str:
    """Normaliza fecha a YYYY-MM-DD.

    Acepta YYYY-MM-DD o DD/MM/YYYY.
    """
    raw = raw.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Formato de fecha no soportado: {raw}")


def parse_whatsapp_message(message: str) -> Movimiento:
    """Parsea un mensaje simple de WhatsApp tipo key:value por línea."""
    fields: dict[str, str] = {}
    for line in message.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower()] = value.strip()

    required = ["fecha", "descripcion", "referencia_1", "valor"]
    missing = [k for k in required if k not in fields]
    if missing:
        raise ValueError(f"Faltan campos requeridos: {', '.join(missing)}")

    fecha = normalize_date(fields["fecha"])
    descripcion = fields["descripcion"].strip()
    referencia_1 = fields["referencia_1"].strip()
    valor = parse_amount_cop(fields["valor"])

    monto_entrada = valor if valor > 0 else 0
    monto_salida = abs(valor) if valor < 0 else 0

    dedup_seed = f"{fecha}|{referencia_1}|{valor}|{descripcion.lower()}"
    id_unico = hashlib.sha256(dedup_seed.encode("utf-8")).hexdigest()[:20]

    return Movimiento(
        fecha=fecha,
        descripcion=descripcion,
        referencia_1=referencia_1,
        valor_original=valor,
        monto_entrada=monto_entrada,
        monto_salida=monto_salida,
        id_unico=id_unico,
    )
