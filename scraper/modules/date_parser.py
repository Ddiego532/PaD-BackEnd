from datetime import datetime, date
import locale
locale.setlocale(locale.LC_TIME, 'es_ES')

# parsear a dd/mm/yy.
def parse_date(raw_date : str, parsing_form : str):
    try:
        # Parsear la fecha original
        date_parsed = datetime.strptime(raw_date, parsing_form)

        # Formatear la nueva fecha en el formato deseado
        return date_parsed.strftime("%d/%m/%Y")
    except ValueError as e:
        return date.today().strftime("%d/%m/%Y")