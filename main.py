from src.pipeline import (
    create_plots,
    download_data,
    generate_statistics,
    preprocess_data,
)


def main():
    print("=== URUCHAMIANIE PIPELINE'U ANALIZY EEG ===\n")

    # 1. Pobieranie / Generowanie struktury danych
    raw_data = download_data()

    # 2. Czyszczenie i filtrowanie sygnału
    processed_data = preprocess_data(raw_data)

    # 3. Wyliczanie statystyk opisowych
    generate_statistics(processed_data)

    # 4. Generowanie wykresów wynikowych
    create_plots(processed_data)

    print("\n=== POTOK PRZETWARZANIA ZAKOŃCZONY SUKCESEM ===")


if __name__ == "__main__":
    main()