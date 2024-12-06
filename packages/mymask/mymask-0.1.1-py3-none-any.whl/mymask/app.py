import sys
import numpy as np
import pandas as pd
from astropy.io import fits
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox,
                             QFileDialog, QPushButton, QComboBox, QLabel, QHBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
import matplotlib.pyplot as plt
import os

class InteractiveSpectrumMaskApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.x = None
        self.y = None
        self.mask = None
        self.data = None  # Holds the full data from the FITS or CSV file
        self.hdul = None  # Holds the HDU list for saving purposes (for FITS)
        self.cid = None  # Initialize the event connection ID
        self.file_path = None  # To store the loaded file path

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interactive Spectrum Mask Tool')
        self.resize(1000, 600)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Main layout
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Top layout for buttons and selectors
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        # Load Data Button
        self.load_button = QPushButton('Load Data (FITS or CSV)', self)
        self.load_button.setFont(QFont('Arial', 10))
        self.load_button.setMinimumWidth(200)
        self.load_button.clicked.connect(self.load_data)
        top_layout.addWidget(self.load_button)

        # X Column Selector
        self.x_selector_label = QLabel('Select X Column:', self)
        self.x_selector_label.setFont(QFont('Arial', 10))
        top_layout.addWidget(self.x_selector_label)
        self.x_selector = QComboBox(self)
        self.x_selector.setMinimumWidth(150)
        self.x_selector.setFont(QFont('Arial', 10))
        top_layout.addWidget(self.x_selector)

        # Y Column Selector
        self.y_selector_label = QLabel('Select Y Column:', self)
        self.y_selector_label.setFont(QFont('Arial', 10))
        top_layout.addWidget(self.y_selector_label)
        self.y_selector = QComboBox(self)
        self.y_selector.setMinimumWidth(150)
        self.y_selector.setFont(QFont('Arial', 10))
        top_layout.addWidget(self.y_selector)

        self.x_selector.currentIndexChanged.connect(self.update_columns)
        self.y_selector.currentIndexChanged.connect(self.update_columns)

        # Save Masked Data Button
        self.save_button = QPushButton('Save Mask', self)
        self.save_button.setFont(QFont('Arial', 10))
        self.save_button.setMinimumWidth(200)
        self.save_button.clicked.connect(self.save_data)
        self.save_button.setEnabled(False)
        top_layout.addWidget(self.save_button)

        # Add top layout to the main layout
        main_layout.addLayout(top_layout)

        # Create the matplotlib Figure and FigCanvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setMinimumHeight(400)
        main_layout.addWidget(NavigationToolbar(self.canvas, self))
        main_layout.addWidget(self.canvas)

        self.ax.set_title('Left-click to mask, right-click to unmask')
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_click)

    def load_data(self):
        # Load data from a FITS or CSV file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Data File', '', 'FITS Files (*.fits);;CSV Files (*.csv);;All Files (*)', options=options)
        if file_path:
            self.file_path = file_path
            if file_path.endswith('.fits'):
                self.load_fits_data(file_path)
            elif file_path.endswith('.csv'):
                self.load_csv_data(file_path)

    def load_fits_data(self, file_path):
        self.hdul = fits.open(file_path)
        data = self.hdul[1].data
        self.data = data
        columns = data.columns.names
        self.x_selector.clear()
        self.y_selector.clear()
        self.x_selector.addItems(columns)
        self.y_selector.addItems(columns)
        # Set default values for x and y to be the first two columns
        if len(columns) >= 2:
            self.x_selector.setCurrentIndex(0)
            self.y_selector.setCurrentIndex(1)
        self.update_columns(initial=True)

    def load_csv_data(self, file_path):
        df = pd.read_csv(file_path)
        self.data = df
        columns = df.columns.tolist()
        self.x_selector.clear()
        self.y_selector.clear()
        self.x_selector.addItems(columns)
        self.y_selector.addItems(columns)
        # Set default values for x and y to be the first two columns
        if len(columns) >= 2:
            self.x_selector.setCurrentIndex(0)
            self.y_selector.setCurrentIndex(1)
        self.update_columns(initial=True)

    def update_columns(self, initial=False):
        if self.data is not None:
            x_col = self.x_selector.currentText()
            y_col = self.y_selector.currentText()
            if x_col and y_col:
                try:
                    if isinstance(self.data, pd.DataFrame):
                        self.x = np.array(self.data[x_col], dtype=float)
                        self.y = np.array(self.data[y_col], dtype=float)
                    else:  # FITS data
                        self.x = np.array(self.data[x_col], dtype=float)
                        self.y = np.array(self.data[y_col], dtype=float)
                    # Remove NaN values from x and y
                    # valid_indices = ~(np.isnan(self.x) | np.isnan(self.y))
                    # self.x = self.x[valid_indices]
                    # self.y = self.y[valid_indices]
                    self.mask = np.ones(len(self.x), dtype=bool)  # Initial mask, all points are valid
                    self.update_plot(initial=initial)
                    self.save_button.setEnabled(True)
                except ValueError:
                    print(f"Could not convert columns '{x_col}' or '{y_col}' to numeric values. Please select valid numeric columns.")

    def on_click(self, event):
        if event.inaxes != self.ax or self.x is None or self.y is None:
            return
        # Get the coordinates of the click in display space
        click_x_display, click_y_display = event.x, event.y

        # Transform data coordinates to display coordinates
        # valid_indices = ~(np.isnan(self.x) | np.isnan(self.y))
        display_coords = self.ax.transData.transform(np.column_stack((self.x, self.y)))
        distances = np.sqrt((display_coords[:, 0] - click_x_display) ** 2 + (display_coords[:, 1] - click_y_display) ** 2)
        ind = np.nanargmin(distances)

        # Mask or unmask the selected point based on mouse button
        if distances[ind] < 10:  # Threshold in pixels for selecting a point
            if event.button == 1:  # Left click to mask
                self.mask[ind] = False
            elif event.button == 3:  # Right click to unmask
                self.mask[ind] = True
            self.update_plot()

    def update_plot(self, initial=False):
        # Store current x and y limits if not the initial plot
        if not initial:
            x_limits = self.ax.get_xlim()
            y_limits = self.ax.get_ylim()

        # Clear and replot the data with the mask applied
        self.ax.clear()
        self.ax.set_title('Left-click to mask, right-click to unmask')
        # Plot the line connecting unmasked points
        if np.any(self.mask):
            self.ax.plot(self.x[self.mask], self.y[self.mask], c='b', linestyle='-', linewidth=1, label='Unmasked Line')
        # Plot the points, smaller size for unmasked and masked points
        if np.any(self.mask):
            self.ax.scatter(self.x[self.mask], self.y[self.mask], c='b', s=10, picker=True, label='Unmasked Points')
        if np.any(~self.mask):
            self.ax.scatter(self.x[~self.mask], self.y[~self.mask], c='r', s=10, alpha=0.5, label='Masked Points')
        self.ax.legend()

        # Restore the previous x and y limits if not the initial plot
        if not initial:
            self.ax.set_xlim(x_limits)
            self.ax.set_ylim(y_limits)
        else:
            self.ax.relim()  # Recompute the data limits for the initial plot
            self.ax.autoscale()  # Autoscale to fit the data

        self.canvas.draw()
        # Reconnect the event handler to ensure it remains active after the plot update
        if self.cid is not None:
            self.canvas.mpl_disconnect(self.cid)  # Disconnect the previous event handler if any
        self.cid = self.canvas.mpl_connect('button_press_event', self.on_click)

    def save_data(self):
        if self.data is None:
            return
        # save the mask into a csv file
        mask_df = pd.DataFrame({'mask': self.mask})
        file_path = self.get_mask_file_path(extension='.csv')
        mask_df.to_csv(file_path, index=False)
        print(f"Mask data saved to {file_path}")

        # post a message window to the user on the GUI
        QMessageBox.information(self, 'Mask Data Saved', f"Mask data saved to {file_path}")

    def get_mask_file_path(self, extension):
        base, ext = os.path.splitext(self.file_path)
        return f"{base}_mask{extension}"

    def closeEvent(self, event):
        # Automatically save the masked data when the application is closed
        self.save_data()
        # Output the masked points when the application is closed
        if self.x is not None and self.y is not None:
            masked_points = np.column_stack((self.x[~self.mask], self.y[~self.mask]))
            print("Masked points:")
            print(masked_points)
        event.accept()

if __name__ == '__main__':
    # Start the Qt application
    app = QApplication(sys.argv)
    app.setStyle('Breeze')  # Set a light, modern style across all platforms
    main_window = InteractiveSpectrumMaskApp()
    main_window.show()
    sys.exit(app.exec_())
