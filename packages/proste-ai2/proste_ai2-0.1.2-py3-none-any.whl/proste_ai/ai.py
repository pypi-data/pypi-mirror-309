import pickle
import os
import warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from .dane import Dane

class AI:
    """Klasa odpowiedzialna za zarządzanie modelami."""
    _show_answers = True  # Włączone podpowiedzi błędów
    _singleton_instance = None  # Singleton dla klasy AI

    def __init__(self):
        """Inicjalizacja atrybutów klasy AI."""
        if AI._singleton_instance:
            raise Exception("Użyj metody `AI.instance()` zamiast tworzenia obiektu AI!")
        self.modele = {}  # Słownik przechowujący modele
        self.vectorizer = TfidfVectorizer()  # Narzędzie do przetwarzania tekstu

    @staticmethod
    def instance():
        """Zwraca instancję singletona klasy AI."""
        if not AI._singleton_instance:
            AI._singleton_instance = AI()
        return AI._singleton_instance

    @staticmethod
    def _handle_error(komunikat, podpowiedz=None):
        """Obsługuje błędy i wyświetla podpowiedzi, jeśli są włączone."""
        print(f"BŁĄD: {komunikat}")
        if AI._show_answers and podpowiedz:
            print(f"Jak to naprawić: {podpowiedz}")
        exit(1)  # Przerywa program

    @staticmethod
    def _handle_warning(komunikat, podpowiedz=None):
        """Obsługuje ostrzeżenia i wyświetla podpowiedzi, jeśli są włączone."""
        print(f"OSTRZEŻENIE: {komunikat}")
        if AI._show_answers and podpowiedz:
            print(f"Jak to naprawić: {podpowiedz}")

    @staticmethod
    def s_answer_off():
        """Wyłącza podpowiedzi błędów i ostrzeżeń."""
        AI._show_answers = False

    @staticmethod
    def s_answer_on():
        """Włącza podpowiedzi błędów i ostrzeżeń."""
        AI._show_answers = True

    def create_model(self, nazwa, rozmiar):
        """Tworzy nowy model z podaną nazwą i rozmiarem oraz przypisuje dane."""
        if nazwa in self.modele:
            AI._handle_error(f"Model o nazwie '{nazwa}' już istnieje!", "Użyj innej nazwy dla nowego modelu.")
        dane = Dane.get_pary()
        self.modele[nazwa] = {
            "model": MLPClassifier(hidden_layer_sizes=(rozmiar,), max_iter=1000),
            "data": dane
        }
        print(f"Model '{nazwa}' utworzony z rozmiarem: {rozmiar}.")

    def train_model(self, nazwa):
        """Trenuje model na wczytanych danych."""
        if nazwa not in self.modele:
            AI._handle_error(f"Model '{nazwa}' nie istnieje!", "Utwórz model przed treningiem.")

        dane = self.modele[nazwa]["data"]
        pytania = [p[0] for p in dane]
        odpowiedzi = [p[1] for p in dane]

        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always", category=ConvergenceWarning)

                X = self.vectorizer.fit_transform(pytania)
                self.modele[nazwa]["model"].fit(X, odpowiedzi)

                for warning in w:
                    if issubclass(warning.category, ConvergenceWarning):
                        AI._handle_warning(
                            f"Model '{nazwa}' nie zbieżny po maksymalnych iteracjach (1000).",
                            "Zwiększ liczbę iteracji `max_iter` lub sprawdź dane treningowe."
                        )
        except Exception as e:
            AI._handle_error(f"Błąd podczas trenowania modelu: {e}", "Sprawdź, czy dane są poprawne.")
        else:
            print(f"Model '{nazwa}' został wytrenowany.")

    def save_model(self, nazwa):
        """Zapisuje model i wektor TF-IDF do pliku."""
        if nazwa not in self.modele:
            AI._handle_error(f"Model '{nazwa}' nie istnieje!", "Najpierw utwórz model przed zapisaniem.")
        try:
            sciezka = f"{nazwa}.pkl"
            with open(sciezka, 'wb') as f:
                pickle.dump({
                    "model": self.modele[nazwa]["model"],
                    "vectorizer": self.vectorizer
                }, f)
            print(f"Model '{nazwa}' zapisany do pliku '{sciezka}'.")
        except Exception as e:
            AI._handle_error(f"Błąd podczas zapisywania modelu: {e}", "Sprawdź prawa dostępu do plików.")

    def wczytaj_model(self, nazwa, plik):
        """Wczytuje model i wektor TF-IDF z pliku."""
        if not os.path.exists(plik):
            AI._handle_error(
                f"Plik '{plik}' nie istnieje!",
                "Upewnij się, że plik istnieje w podanej ścieżce i ma poprawną nazwę."
            )
        try:
            with open(plik, 'rb') as f:
                dane = pickle.load(f)
                self.modele[nazwa] = {"model": dane["model"]}
                self.vectorizer = dane["vectorizer"]
            print(f"Model '{nazwa}' wczytany z pliku '{plik}'.")
        except Exception as e:
            AI._handle_error(
                f"Błąd podczas wczytywania modelu: {e}",
                "Sprawdź, czy plik modelu jest poprawny i czy nie jest uszkodzony."
            )

    def use(self, prompt, nazwa):
        """Używa modelu do generowania odpowiedzi na podstawie promptu."""
        if nazwa not in self.modele:
            AI._handle_error(
                f"Model '{nazwa}' nie istnieje!",
                "Utwórz lub wczytaj model przed użyciem."
            )
        try:
            model = self.modele[nazwa]["model"]
            X = self.vectorizer.transform([prompt])
            odpowiedz = model.predict(X)
            return odpowiedz[0]
        except Exception as e:
            AI._handle_error(
                f"Błąd podczas używania modelu: {e}",
                "Sprawdź, czy model został poprawnie wytrenowany i czy dane wejściowe są odpowiednie."
            )
