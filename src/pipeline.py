import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def download_data(output_dir="data"):
    import mne
    print("Pobieranie prawdziwych danych EEG z serwerów PhysioNet...")
    
    # 1. Pobieranie danych z bazy PhysioNet
    physionet_paths = mne.datasets.eegbci.load_data(subjects=1, runs=[4], update_path=False)
    raw = mne.io.read_raw_edf(physionet_paths[0], preload=True, verbose=False)
    
    # 2. Wybór centralnego kanału i wycięcie 2500 punktów
    target_channel = 'Fcza.' if 'Fcza.' in raw.ch_names else raw.ch_names[0]
    eeg_signal = raw.get_data(picks=target_channel)[0][:2500] * 1e6 # Skalowanie do uV
    
    # 3. Tworzenie czasu (osi X)
    fs = int(raw.info['sfreq'])
    t = np.linspace(0, len(eeg_signal) / fs, len(eeg_signal), endpoint=False)
    
    # 4. Budowanie DataFrame, którego oczekuje reszta programu autora
    df = pd.DataFrame({"Time": t, "EEG_Channel_1": eeg_signal})
    
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "eeg_signal.txt")
    df.to_csv(file_path, index=False)
    
    print(f"Prawdziwe dane zostały zapisane w: {file_path}")
    return df

def preprocess_data(df):
    print("Rozpoczęcie wstępnego przetwarzania prawdziwego sygnału EEG...")
    
    # Kopia danych, aby nie psuć oryginału
    processed_df = df.copy()
    
    # Filtrowanie średnią kroczącą (tak jak chciał autor)
    window_size = 7
    processed_df['EEG_Filtered'] = processed_df['EEG_Channel_1'].rolling(window=window_size, center=True).mean()
    
    # Uzupełniamy puste miejsca na brzegach po filtracji, żeby program się nie wywalił
    processed_df.bfill(inplace=True)
    processed_df.ffill(inplace=True)
    
    return processed_df

def generate_statistics(df):
    print("\n--- STATYSTYKI OPISOWE PRAWDZIWEGO SYGNAŁU EEG ---")
    stats_df = df[['EEG_Channel_1', 'EEG_Filtered']]
    print(stats_df.describe())

def create_plots(df, output_dir="data"):
    print("Generowanie nowych wykresów z prawdziwymi danymi EEG...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Wykres sygnału surowego i przefiltrowanego
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(df['Time'], df['EEG_Channel_1'], color='crimson', alpha=0.7, label='Surowy sygnał z PhysioNet')
    plt.title("Potok Przetwarzania EEG - PRAWDZIWE DANE")
    plt.ylabel("Amplituda [µV]")
    plt.legend()
    plt.grid(True, linestyle='--')
    
    plt.subplot(2, 1, 2)
    plt.plot(df['Time'], df['EEG_Filtered'], color='teal', label='Sygnał po filtracji (Średnia krocząca)')
    plt.xlabel("Czas [sekundy]")
    plt.ylabel("Amplituda [µV]")
    plt.legend()
    plt.grid(True, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "wykres_porownawczy.png"), dpi=150)
    plt.close()
    
    # Drugi wykres (sam surowy sygnał)
    plt.figure(figsize=(12, 4))
    plt.plot(df['Time'], df['EEG_Channel_1'], color='darkblue')
    plt.title("Surowy zapis EEG (PhysioNet)")
    plt.xlabel("Czas [sekundy]")
    plt.ylabel("Amplituda [µV]")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "wykres_sygnalu.png"), dpi=150)
    plt.close()
    