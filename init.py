import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import find_peaks
import mplcursors
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Análisis de Datos")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.load_button = QPushButton("Cargar Archivo")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

    def load_data(self):
        self.clear_text()  # Limpiar el área de texto antes de cargar un nuevo archivo

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Archivos CSV (*.csv);;Archivos Excel (*.xlsx)", options=options)
        if file_name:
            self.process_data(file_name)

    def process_data(self, file_name):
        try:
            if file_name.endswith('.csv'):
                data = pd.read_csv(file_name, sep=';')
            elif file_name.endswith('.xlsx'):
                data = pd.read_excel(file_name)
            else:
                self.text_edit.append("Formato de archivo no compatible. Se aceptan archivos CSV y XLSX.")
                return

            self.text_edit.append("Datos cargados correctamente:")
            self.text_edit.append(str(data.head()))

            self.visualize_data(data)
            self.analyze_data(data)
        except Exception as e:
            self.text_edit.append("Error al procesar los datos:")
            self.text_edit.append(str(e))

    def visualize_data(self, data):
        plt.figure(figsize=(10, 7))
        plt.plot(data['Time'], data['PV'], label='PV', color='blue')
        plt.plot(data['Time'], data['SP'], label='SP', color='red')
        plt.plot(data['Time'], data['OP'], label='OP', color='green')
        plt.plot(data['Time'], data['Error'], label='Error', color='orange')
        plt.title('Variables del proceso vs Tiempo')
        plt.xlabel('Tiempo')
        plt.ylabel('Valor')
        plt.grid(True)
        plt.legend()
        plt.show()

    def analyze_data(self, data):
        PV = data['PV']
        SP = data['SP']
        OP = data['OP']
        error = data['Error']

        # Integral del error absoluto (IAE)
        IAE = np.sum(np.abs(PV - SP))
        IAElim = 100

        if IAE > IAElim:
            self.text_edit.append("❎ -----> El proceso presenta oscilaciones significativas con el metodo IAE")
        else:
            self.text_edit.append("✅ -----> El proceso no presenta oscilaciones significativas con el metodo IAE")

        # Media, desviación estándar y covarianza de las variables
        mean_PV = np.mean(PV)
        mean_OP = np.mean(OP)
        covariance_OP = np.cov(OP)
        covariance_PV = np.cov(PV)
        std_PV = np.std(PV)
        std_OP = np.std(OP)

        self.text_edit.append(f"Desviación estándar de PV: {std_PV}")
        self.text_edit.append(f"Desviación estándar de OP: {std_OP}")
        self.text_edit.append(f"Covarianza de OP: {covariance_OP}")
        self.text_edit.append(f"Covarianza de PV: {covariance_PV}")
        self.text_edit.append(f"Media de PV: {mean_PV}")
        self.text_edit.append(f"Media de OP: {mean_OP}")
        self.text_edit.append(f"Valor de IAE: {IAE}")
        self.text_edit.append(f"Límite de IAE (IAElim): {IAElim}")

        # Error absoluto a lo largo del tiempo
        absolute_error = np.abs(PV - SP)
        plt.figure(figsize=(10, 5))
        plt.plot(data['Time'], absolute_error, marker='o', linestyle='-')
        plt.title('Error Absoluto a lo Largo del Tiempo')
        plt.xlabel('Tiempo')
        plt.ylabel('Error Absoluto')
        plt.grid(True)
        plt.show()
        
        # Calcular la transformada de Fourier
        pv_values = data['PV'].values 
        spectrum = fft(pv_values) 

        # Calcular el espectro de potencia
        power_spectrum = np.abs(spectrum) ** 2

        # Encontrar picos en el espectro de potencia
        peaks, _ = find_peaks(power_spectrum, distance=20)  # ajusta la distancia según tus necesidades

        # Visualizar el espectro de potencia y los picos
        plt.figure(figsize=(10, 5))
        plt.plot(power_spectrum, label='Espectro de Potencia')
        plt.plot(peaks, power_spectrum[peaks], 'ro', label='Picos')
        plt.title('Espectro de Potencia y Detección de Picos')
        plt.xlabel('Frecuencia')
        plt.ylabel('Potencia')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Imprimir los índices de las frecuencias correspondientes a los picos
        self.text_edit.append("Índices de frecuencias correspondientes a los picos:")
        self.text_edit.append(str(peaks))


                
        # Definir umbral para la autocovarianza
        umbral_acf = 2  #  puedes ajustar este valor según tus necesidades

        # Análisis en el dominio del tiempo utilizando ACF
        acf = np.correlate(PV, PV, mode='full') / len(PV)
        time_lags = np.arange(-len(PV) + 1, len(PV))

        plt.figure(figsize=(10, 5))
        plt.stem(time_lags, acf)
        plt.title('Autocovarianza en el Dominio del Tiempo')
        plt.xlabel('Desfase')
        plt.ylabel('Autocovarianza')
        plt.grid(True)

        # Determinar si hay perturbaciones basadas en el umbral
        if np.max(acf) > umbral_acf:
            plt.axhline(y=umbral_acf, color='r', linestyle='--', label=f'Umbral ACF ({umbral_acf})')
            plt.legend()
            self.text_edit.append("❎ -----> Se encontraron perturbaciones utilizando ACF.")
        else:
            self.text_edit.append("✅ -----> No se encontraron perturbaciones utilizando ACF.")

        plt.show()


    def clear_text(self):
        self.text_edit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
