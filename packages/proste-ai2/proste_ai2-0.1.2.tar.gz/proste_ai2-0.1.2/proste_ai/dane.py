import csv
from .ai import AI  # Aby obsługiwać błędy i ostrzeżenia AI

class Dane:
    """Klasa odpowiedzialna za wczytywanie danych."""
    _pary = []  # Przechowuje dane w formacie pytanie-odpowiedź

    @staticmethod
    def wczytaj_pary_csv(plik, separator=";"):
        """Statyczna metoda wczytująca dane z pliku CSV."""
        try:
            with open(plik, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=separator)
                Dane._pary = []  # Reset danych
                for i, wiersz in enumerate(reader, start=1):  # start=1 dla numeracji od 1
                    if len(wiersz) < 2:
                        AI._handle_error(
                            f"Błąd w pliku CSV w linijce {i}: za mało kolumn.",
                            f"Sprawdź linijkę {i} w pliku {plik}. Powinna zawierać pytanie i odpowiedź oddzielone '{separator}'."
                        )
                    Dane._pary.append((wiersz[0], wiersz[1]))
            print(f"Wczytano {len(Dane._pary)} par danych z pliku {plik}.")
        except FileNotFoundError:
            AI._handle_error(
                f"Plik '{plik}' nie istnieje.",
                "Upewnij się, że plik istnieje w podanej ścieżce."
            )
        except Exception as e:
            AI._handle_error(
                f"Błąd podczas wczytywania danych: {e}",
                "Sprawdź poprawność pliku CSV i separator."
            )

    @staticmethod
    def get_pary():
        """Zwraca załadowane dane. Informuje o błędzie, jeśli dane nie zostały wczytane."""
        if not Dane._pary:
            AI._handle_error(
                "Brak wczytanych danych.",
                "Użyj metody `Dane.wczytaj_pary_csv()` przed próbą uzyskania dostępu do danych."
            )
        return Dane._pary
