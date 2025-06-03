from bank_parsers.bank_pdf_parser_class import BankPDFParser
from bank_parsers.davivienda_pdf_parser import DaviviendaPDFParser
from bank_parsers.rappi_pdf_parser import RappiPDFParser
from bank_parsers.nu_pdf_parser import NuPDFParser
from bank_parsers.bancolombia_pdf_parser import BancolombiaPDFParser
from .monex_pdf_parser import MonexPDFParser

bank_parsers_list = {
    "Davivienda": {
        "Ahorros": DaviviendaPDFParser(),
    },
    "Rappi": {
        "Credito": RappiPDFParser(),
    },
    "Nu": {
        "Credito": NuPDFParser(),
    },
    "Bancolombia": {
        "Ahorros": BancolombiaPDFParser(),
    },
    "Monex": {
        "Cuenta MXN": MonexPDFParser(),
    },
}


def make_bank_parser(bank, acc_type) -> BankPDFParser:
    return bank_parsers_list[bank][acc_type]
