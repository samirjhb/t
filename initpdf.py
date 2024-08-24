import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.signal import find_peaks
import mplcursors
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTextEdit
from fpdf import FPDF
from os.path import exists

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
        
        self.pdf_button = QPushButton("Generar Informe PDF")
        self.pdf_button.clicked.connect(self.generate_pdf_report)
        self.layout.addWidget(self.pdf_button)

        # Inicialización de atributos
        self.data = None
        self.IAE = None
        self.mean_frequency = None
        self.mean_amplitude = None
        self.perturbations_IAE = None
        self.perturbations_ACF = None
        self.mean_frequency = None
        self.mean_amplitude = None
        self.covariance_OP = None
        self.covariance_PV = None
        self.std_PV = None
        self.std_OP = None
        self.mean_PV = None
        self.mean_OP = None
        self.IAElim = None

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
                self.data = pd.read_csv(file_name, sep=',')
            elif file_name.endswith('.xlsx'):
                data = pd.read_excel(file_name)
                self.data = pd.read_excel(file_name)
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

    def visualize_data(self, data, save=False, filename="variables_vs_tiempo.png"):
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
        if save:
            plt.savefig(filename)
            plt.close()
        else:
            plt.show()

    def analyze_data(self, data, save=False):
        PV = data['PV']
        SP = data['SP']
        OP = data['OP']
        error = data['Error']

        # Integral del error absoluto (IAE)
        IAE = np.sum(np.abs(PV - SP))
        self.IAE = IAE
        IAElim = 100
        self.IAElim=IAElim

        if IAE > IAElim:
            self.text_edit.append("❎ -----> El proceso presenta oscilaciones significativas con el método IAE")
            self.perturbations_IAE = "El proceso presenta oscilaciones significativas"
        else:
            self.text_edit.append("✅ -----> El proceso no presenta oscilaciones significativas con el método IAE")
            self.perturbations_IAE = "El proceso no presenta oscilaciones significativas"

        # Media, desviación estándar y covarianza de las variables
        mean_PV = np.mean(PV)
        mean_OP = np.mean(OP)
        covariance_OP = np.cov(OP)
        covariance_PV = np.cov(PV)
        std_PV = np.std(PV)
        std_OP = np.std(OP)
        self.mean_frequency = np.mean(PV)
        self.mean_amplitude = np.mean(OP)
        self.covariance_OP = covariance_OP
        self.covariance_PV = covariance_PV
        self.std_PV = std_PV
        self.std_OP = std_OP
        self.mean_PV = mean_PV
        self.mean_OP = mean_OP



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
        if save:
            plt.savefig("error_absoluto.png")
            plt.close()  # Cerrar la figura después de guardar
        else:
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
        if save:
            plt.savefig("espectro_potencia.png")
            plt.close()  # Cerrar la figura después de guardar
        else:
            plt.show()

        # Análisis en el dominio del tiempo utilizando ACF
        umbral_acf = 2  # Define el umbral para la autocovarianza

        acf = np.correlate(PV, PV, mode='full') / len(PV)
        time_lags = np.arange(-len(PV) + 1, len(PV))

        plt.figure(figsize=(10, 5))
        plt.stem(time_lags, acf)
        plt.title('Autocovarianza en el Dominio del Tiempo')
        plt.xlabel('Desfase')
        plt.ylabel('Autocovarianza')
        plt.grid(True)
        if np.max(acf) > umbral_acf:
            plt.axhline(y=umbral_acf, color='r', linestyle='--', label=f'Umbral ACF ({umbral_acf})')
            plt.legend()
            self.text_edit.append("❎ -----> Se encontraron perturbaciones utilizando ACF.")
            self.perturbations_ACF = "Se encontraron perturbaciones"
        else:
            self.text_edit.append("✅ -----> No se encontraron perturbaciones utilizando ACF.")
            self.perturbations_ACF = "No se encontraron perturbaciones"
        if save:
            plt.savefig("autocovarianza.png")
            plt.close()  # Cerrar la figura después de guardar
        else:
            plt.show()

    def clear_text(self):
        self.text_edit.clear()

    def generate_pdf_report(self):
        # Verifica si todos los datos necesarios están presentes
        if (self.data is None or 
            self.IAE is None or 
            self.mean_frequency is None or 
            self.mean_amplitude is None or 
            self.perturbations_IAE is None or 
            self.perturbations_ACF is None):
            self.text_edit.append(f"Datos de análisis:\n"
                                  f"IAE: {self.IAE}\n"
                                  f"Media de frecuencias: {self.mean_frequency}\n Hz"
                                  f"Media de amplitudes: {self.mean_amplitude}\n"
                                  f"Perturbaciones IAE: {self.perturbations_IAE}\n"
                                  f"Perturbaciones ACF: {self.perturbations_ACF}\n")
            self.text_edit.append("No hay datos cargados para generar el informe.")
            return

        try:
            pdf = FPDF()

            # Página de Datos Básicos del Análisis
            self._generate_report_page(pdf, "Datos Básicos del Análisis", [
                        f"Desviación estándar de PV: {self.std_PV}\n"
                        f"Desviación estándar de OP: {self.std_OP}\n"
                        f"Covarianza de OP: {self.covariance_OP}\n"
                        f"Covarianza de PV: {self.covariance_PV}\n"
                        f"Valor de IAE: {self.IAE}\n"
                        f"Límite de IAE (IAElim): {self.IAElim}\n"
                        f"Media de PV: {self.mean_frequency}Hz\n "
                        f"Media de OP: {self.mean_amplitude}\n"
                        f"Perturbaciones IAE: {self.perturbations_IAE}\n"
                        f"Perturbaciones ACF: {self.perturbations_ACF}\n"
            ])

            # Guardar imágenes antes de agregarlas al PDF
            self.visualize_data(self.data, save=True, filename="variables_vs_tiempo.png")
            self.analyze_data(self.data, save=True)  # Esto debe guardar las imágenes necesarias

            # Verificar si las imágenes existen
            images = ["variables_vs_tiempo.png", "error_absoluto.png", "espectro_potencia.png", "autocovarianza.png"]
            for image in images:
                if not exists(image):
                    self.text_edit.append(f"Error: La imagen {image} no se encontró.")
                    return

            # Agregar imágenes al PDF
            self._generate_report_page(pdf, "Variables del Proceso vs Tiempo", "variables_vs_tiempo.png")
            self._generate_report_page(pdf, "Error Absoluto a lo Largo del Tiempo", "error_absoluto.png")
            self._generate_report_page(pdf, "Espectro de Potencia y Detección de Picos", "espectro_potencia.png")
            self._generate_report_page(pdf, "Autocovarianza en el Dominio del Tiempo", "autocovarianza.png")

            pdf_output_path = QFileDialog.getSaveFileName(self, "Guardar Informe PDF", "", "Archivos PDF (*.pdf)")[0]
            if pdf_output_path:
                pdf.output(pdf_output_path)
                self.text_edit.append("Informe PDF generado correctamente.")
        except Exception as e:
            self.text_edit.append(f"Error al generar el informe PDF: {str(e)}")

    def _generate_report_page(self, pdf, title, content):
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        pdf.cell(200, 10, txt = title, ln = True, align = 'C')
        if isinstance(content, list):
            for line in content:
                pdf.multi_cell(0, 10, txt = line)
        else:
            pdf.image(content, x = 10, y = 20, w = 180)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

