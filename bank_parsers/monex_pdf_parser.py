import pdfplumber
from pathlib import Path
import pandas as pd
import re
from bank_parsers.bank_pdf_parser_class import BankPDFParser


class MonexPDFParser(BankPDFParser):
    resultados_list = ["movimientos"]

    def parse_pdf(self, input_path: Path, password: str):
        movimientos = []
        date_pattern = re.compile(r"\d{2}/\d{2}/\d{4}")
        with pdfplumber.open(input_path, password=password) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables or []:
                    for row in table:
                        if not row:
                            continue
                        if any(cell and "Fecha" in cell for cell in row):
                            continue
                        fila = [cell.strip() if cell else "" for cell in row]
                        if not date_pattern.match(fila[0]):
                            continue
                        # Ensure length at least 6
                        while len(fila) < 6:
                            fila.append("")
                        movimientos.append(
                            {
                                "Fecha": fila[0],
                                "Descripción": fila[1],
                                "Referencia": fila[2],
                                "Abono": fila[3],
                                "Cargo": fila[4],
                                "Saldo Disponible": fila[5],
                            }
                        )
        return movimientos

    def process(self, movimientos):
        df = pd.DataFrame(movimientos)
        for col in ["Abono", "Cargo", "Saldo Disponible"]:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("$", "")
                .str.replace(",", "")
                .str.replace(" ", "")
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return [df]
