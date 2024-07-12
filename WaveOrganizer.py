import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QMessageBox, QFileDialog, QLineEdit, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_path = ''
        self.target_folder = ''
        self.initUI()

    def initUI(self):
        # Layout for base path selection
        basePathLayout = QHBoxLayout()
        self.basePathButton = QPushButton("Select WAVE Folder")
        self.basePathButton.clicked.connect(self.set_base_path)
        self.basePathText = QLineEdit()
        self.basePathText.setPlaceholderText("Enter or select base path")
        self.basePathText.setReadOnly(True)  # Make the text box read-only
        basePathLayout.addWidget(self.basePathButton)
        basePathLayout.addWidget(self.basePathText)

        # Layout for target folder selection
        targetFolderLayout = QHBoxLayout()
        self.targetFolderButton = QPushButton("Select Destination Folder")
        self.targetFolderButton.clicked.connect(self.set_target_folder)
        self.targetFolderText = QLineEdit()
        self.targetFolderText.setPlaceholderText("Enter or select target folder")
        self.targetFolderText.setReadOnly(True)  # Make the text box read-only
        targetFolderLayout.addWidget(self.targetFolderButton)
        targetFolderLayout.addWidget(self.targetFolderText)

        # Text edit for file list
        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Paste your file list here...")

        # Execute button
        self.executeButton = QPushButton("Execute")
        self.executeButton.clicked.connect(self.move_files)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(basePathLayout)
        layout.addLayout(targetFolderLayout)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.executeButton)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Window properties
        self.setWindowTitle('File Mover')
        self.setGeometry(300, 300, 600, 400)
        self.show()

    def set_base_path(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Base Path")
        if directory:
            self.base_path = directory
            self.basePathText.setText(directory)  # Update text box with selected path

    def set_target_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Target Folder")
        if directory:
            self.target_folder = directory
            self.targetFolderText.setText(directory)  # Update text box with selected path

    def move_files(self):
        self.base_path = self.basePathText.text()  # Get the path from text box
        self.target_folder = self.targetFolderText.text()  # Get the path from text box
        file_list = self.textEdit.toPlainText().splitlines()

        if not self.base_path or not self.target_folder:
            QMessageBox.warning(self, "Path Not Set", "Please set both base path and target folder before executing.")
            return

        if not file_list:
            QMessageBox.warning(self, "Empty File List", "Please enter at least one filename into the text box.")
            return

        try:
            if not os.path.exists(self.target_folder):
                os.makedirs(self.target_folder)

            moved_files = 0
            for dirpath, dirnames, filenames in os.walk(self.base_path):
                for filename in filenames:
                    if filename.endswith('.wav'):
                        filename_without_extension = filename[:-4]
                        if filename_without_extension in file_list:
                            file_path = os.path.join(dirpath, filename)
                            target_path = os.path.join(self.target_folder, filename)
                            shutil.move(file_path, target_path)
                            moved_files += 1

            QMessageBox.information(self, "Operation Complete", f"Moved {moved_files} files.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()