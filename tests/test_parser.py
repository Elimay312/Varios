import unittest

from bank_automation.parser import normalize_date, parse_amount_cop, parse_whatsapp_message


class ParserTests(unittest.TestCase):
    def test_parse_amount_positive(self):
        self.assertEqual(parse_amount_cop("COP $70.000"), 70000)

    def test_parse_amount_negative(self):
        self.assertEqual(parse_amount_cop("COP -$7.187.000"), -7187000)

    def test_normalize_date(self):
        self.assertEqual(normalize_date("12/02/2026"), "2026-02-12")

    def test_parse_whatsapp_message(self):
        message = """
fecha: 2026-02-12
descripcion: Pago qr
referencia_1: 0069814846
valor: COP -$30.000
""".strip()
        mov = parse_whatsapp_message(message)
        self.assertEqual(mov.monto_entrada, 0)
        self.assertEqual(mov.monto_salida, 30000)
        self.assertTrue(mov.id_unico)


if __name__ == "__main__":
    unittest.main()
