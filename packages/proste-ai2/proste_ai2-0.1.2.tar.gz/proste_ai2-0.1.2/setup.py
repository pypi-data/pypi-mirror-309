from setuptools import setup, find_packages

setup(
    name="proste_ai2",                    # Nazwa pakietu
    version="0.1.2",                     # Wersja
    description="Prosty pakiet AI do nauki",  # Krótki opis
    long_description=open("README.md").read(),  # Długi opis (z README.md)
    long_description_content_type="text/markdown",  # Typ długiego opisu
    author="Situus",                 # Twoje imię lub pseudonim
    author_email="situs1235@gmail.com",  # Twój email
    license="MIT",                       # Licencja projektu
    packages=find_packages(),            # Automatyczne wykrywanie modułów
    install_requires=[                   # Wymagane zależności
        "scikit-learn>=1.0",
    ],
    python_requires=">=3.7",             # Minimalna wersja Pythona
    classifiers=[                        # Klasyfikatory
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
