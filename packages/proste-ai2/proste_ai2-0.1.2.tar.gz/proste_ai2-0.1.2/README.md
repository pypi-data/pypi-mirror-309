# Proste AI
Proste AI to prosty pakiet AI w Pythonie, który umożliwia zarządzanie danymi, tworzenie modeli oraz generowanie odpowiedzi na podstawie wytrenowanego modelu. Pakiet obsługuje wczytywanie danych z plików CSV, trenowanie modeli i ich zapis oraz późniejsze wykorzystanie.

Instalacja
Najpierw zainstaluj pakiet za pomocą pip:

pip install proste-ai
Funkcje
Pakiet składa się z dwóch głównych klas:

Dane: Zarządza wczytywaniem i przechowywaniem danych.
AI: Zarządza modelami AI, ich tworzeniem, trenowaniem, zapisywaniem i wczytywaniem.
1. Dane.wczytaj_pary_csv(plik, separator=";")
Wczytuje dane z pliku CSV w formacie: pytanie;odpowiedź. Separator można zmienić, jeśli plik CSV używa innego.

Przykład:

from proste_ai import Dane

Dane.wczytaj_pary_csv("dane.csv", ";")  # Wczytaj dane z pliku
2. Dane.get_pary()
Zwraca załadowane dane w postaci listy par (pytanie, odpowiedź).

Przykład:

from proste_ai import Dane

Dane.wczytaj_pary_csv("dane.csv", ";")
pary = Dane.get_pary()
print(pary)  # Wyświetli wczytane dane
3. AI.create_model(nazwa, rozmiar)
Tworzy nowy model o podanej nazwie i rozmiarze warstwy ukrytej.

Przykład:

from proste_ai import AI

ai = AI.instance()
ai.create_model("test", 64)  # Tworzy model o nazwie "test" z warstwą ukrytą 64 neuronów
4. AI.train_model(nazwa)
Trenuje model o podanej nazwie na wczytanych danych.

Przykład:

from proste_ai import AI

ai = AI.instance()
ai.train_model("test")  # Trenuje model "test"
5. AI.save_model(nazwa)
Zapisuje model i wektor TF-IDF do pliku o nazwie nazwa.pkl.

Przykład:

from proste_ai import AI

ai = AI.instance()
ai.save_model("test")  # Zapisuje model "test" do pliku "test.pkl"
6. AI.wczytaj_model(nazwa, plik)
Wczytuje model i wektor TF-IDF z pliku o nazwie plik.

Przykład:

from proste_ai import AI

ai = AI.instance()
ai.wczytaj_model("test", "test.pkl")  # Wczytuje model "test" z pliku "test.pkl"
7. AI.use(prompt, nazwa)
Generuje odpowiedź na podstawie podanego promptu (pytania) za pomocą modelu o nazwie nazwa.

Przykład:

from proste_ai import AI

ai = AI.instance()
odpowiedź = ai.use("Cześć, jak się masz?", "test")
print(odpowiedź)  # Wyświetli odpowiedź wygenerowaną przez model
8. AI.s_answer_on() / AI.s_answer_off()
Włącza lub wyłącza podpowiedzi błędów i ostrzeżeń.

Przykład:

from proste_ai import AI

AI.s_answer_off()  # Wyłącza podpowiedzi
AI.s_answer_on()   # Włącza podpowiedzi
Pełny przykład użycia
from proste_ai import Dane, AI

# Wczytanie danych z pliku CSV
Dane.wczytaj_pary_csv("dane.csv", ";")

# Tworzenie i trenowanie modelu
ai = AI.instance()
ai.create_model("test", 64)
ai.train_model("test")

# Zapisanie modelu
ai.save_model("test")

# Wczytanie modelu
ai.wczytaj_model("test", "test.pkl")

# Generowanie odpowiedzi
prompt = input("Podaj pytanie: ")
odpowiedź = ai.use(prompt, "test")
print("Odpowiedź:", odpowiedź)