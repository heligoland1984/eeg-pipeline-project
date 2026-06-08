# Potok Przetwarzania i Oczyszczania Sygnałów EEG

## Opis projektu
Projekt implementuje automatyczny potok (pipeline) do przetwarzania surowych danych neurofizjologicznych (zapis EEG). Program symuluje pobieranie danych ze standardowych baz takich jak PhysioNet, dokonuje cyfrowego filtrowania sygnału (redukcja szumów za pomocą średniej kroczącej), generuje statystyki opisowe amplitudy fal mózgowych oraz tworzy wykresy porównawcze przed i po filtracji.

## Źródło danych
Struktura danych oparta jest na wytycznych repozytoriów takich jak PhysioNet. W celu zapewnienia niezawodności działania bez pobierania wielogigabajtowych plików binarnych, potok generuje oraz analizuje dedykowany, ustrukturyzowany sygnał zawierający symulację przejścia fal Alfa w fale Beta wraz z nałożonym szumem gaussowskim.

## Instrukcja instalacji  
1. Upewnij się, że posiadasz środowisko Python w wersji min. 3.8.  
   `python --version`
2. Pobierz repozytorium:  
   `git clone https://github.com/heligoland1984/eeg-pipeline-project`  
3. Wejdź do katalogu:  
   `cd eeg-pipeline-project`  
4. Zainstaluj wymagane pakiety:  
   `pip install -r requirements.txt`  
5. Uruchom  
   `python main.py`
