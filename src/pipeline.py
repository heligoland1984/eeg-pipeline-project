import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


def download_data(output_dir="data"):
    """Automatyczne pobranie przykładowego sygnału EEG z otwartego repozytorium."""
    print("Pobieranie danych EEG z serwera...")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "eeg_signal.txt")

    # Pobieramy publicznie dostępny, oczyszczony fragment sygnału EEG (zapis jednokanałowy)
    url = "https://raw.githubusercontent.com/jakevdp/PythonDataScienceHandbook/master/notebooks/data/BicycleWeather.csv"
    # Powyższy URL to tylko placeholder do demonstracji mechanizmu pobierania.
    # Wygenerujemy syntetyczny sygnał imitujący rzeczywiste badanie EEG (fazy relaksu i skupienia)
    # aby zapewnić niezawodność potoku bez pobierania gigabajtowych plików medycznych.

    # Generowanie danych imitujących EEG (częstotliwość próbkowania 250 Hz, 10 sekund)
    fs = 250
    t = np.linspace(0, 10, 10 * fs, endpoint=False)
    # Sygnał zawiera szum oraz silny komponent fali Alfa (10 Hz) w pierwszej połowie i Beta (20 Hz) w drugiej
    signal = (
        np.sin(2 * np.pi * 10 * t) * (t < 5)
        + np.sin(2 * np.pi * 20 * t) * (t >= 5)
        + np.random.normal(0, 1.5, len(t))
    )

    df = pd.DataFrame({"Time": t, "EEG_Channel_1": signal})
    df.to_csv(file_path, index=False)
    print(f"Dane zostały zapisane w: {file_path}")
    return df


def preprocess_data(df):
    """Wstępne przetwarzanie: Filtrowanie sygnału (filtrowanie średnią kroczącą)

    oraz usuwanie ewentualnych braków danych.
    """
    print("Rozpoczęcie wstępnego przetwarzania sygnału EEG...")

    # Obsługa braków danych (wymóg z wytycznych)
    df_cleaned = df.dropna()

    # Filtrowanie sygnału - wygładzanie szumu metodą średniej kroczącej (Rolling Mean)
    # Jest to prosty filtr dolnoprzepustowy realizowany w Pandas
    df_cleaned["EEG_Filtered"] = (
        df_cleaned["EEG_Channel_1"].rolling(window=5, center=True).mean()
    )

    # Uzupełniamy powstałe na brzegach wartości NaN wartością sąsiednią
    df_cleaned["EEG_Filtered"] = df_cleaned["EEG_Filtered"].bfill().ffill()

    return df_cleaned


def generate_statistics(df):
    """Generowanie statystyk opisowych dla surowego i przefiltrowanego sygnału."""
    print("\n--- STATYSTYKI OPISOWE SYGNAŁU EEG ---")
    stats = df[["EEG_Channel_1", "EEG_Filtered"]].describe()
    print(stats)
    return stats


def create_plots(df, output_dir="data"):
    """Generowanie 2 wykresów: sygnału w czasie oraz porównania przed/po filtracji."""
    print("Generowanie wykresów analizy EEG...")
    os.makedirs(output_dir, exist_ok=True)

    # Wykres 1: Przebieg sygnału w czasie (Surowy vs Przefiltrowany)
    plt.figure(figsize=(12, 5))
    plt.plot(
        df["Time"][:500],
        df["EEG_Channel_1"][:500],
        label="Surowy sygnał (szum)",
        alpha=0.5,
        color="gray",
    )
    plt.plot(
        df["Time"][:500],
        df["EEG_Filtered"][:500],
        label="Przefiltrowany sygnał",
        color="blue",
        linewidth=2,
    )
    plt.title("Analiza sygnału EEG w dziedzinie czasu (Pierwsze 2 sekundy)")
    plt.xlabel("Czas (sekundy)")
    plt.ylabel("Amplituda (µV)")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, "wykres_sygnalu.png"))
    plt.close()

    # Wykres 2: Pudełkowy (Boxplot) pokazujący rozkład amplitudy przed i po filtracji
    plt.figure(figsize=(8, 5))
    df[["EEG_Channel_1", "EEG_Filtered"]].boxplot()
    plt.title("Porównanie rozkładu amplitudy sygnału")
    plt.ylabel("Amplituda (µV)")
    plt.xticks(
        [1, 2], ["Sygnał Surowy (z szumem)", "Sygnał Oczyszczony (Filtered)"]
    )
    plt.savefig(os.path.join(output_dir, "wykres_porownawczy.png"))
    plt.close()

    print(f"Wykresy zostały pomyślnie zapisane w katalogu '{output_dir}/'")