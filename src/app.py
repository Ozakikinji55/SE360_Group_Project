import os
import sys

from PyQt5.QtCore import QLibraryInfo

#  关键：直接定位到 platforms 目录
plugin_path = os.path.join(
    QLibraryInfo.location(QLibraryInfo.PluginsPath),
    "platforms"
)

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

print("FINAL QT PATH:", plugin_path)

import sys
import time
import os
import re

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit,
    QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QLabel, QMessageBox,
    QFileDialog
)

#  因为你在 src 目录下
sys.path.append(".")

from core.problem import Problem
from solvers.greedy_solver import GreedySolver


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optimal Sample Selection System")
        self.setGeometry(100, 100, 500, 600)

        # File tracking
        self.loaded_file_path = None
        self.results_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "results")
        )

        layout = QVBoxLayout()

        # Parameter inputs
        self.m_input = QLineEdit("45")
        self.n_input = QLineEdit("12")
        self.k_input = QLineEdit("6")
        self.j_input = QLineEdit("5")
        self.s_input = QLineEdit("5")

        # Button row
        self.run_button = QPushButton("Run")
        self.open_button = QPushButton("Open File")
        self.delete_button = QPushButton("Delete File")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.delete_button)

        # Status label
        self.status_label = QLabel("Loaded: (none)")

        # Results area
        self.result_area = QTextEdit()

        # Assemble layout
        for w in [
            self.m_input,
            self.n_input,
            self.k_input,
            self.j_input,
            self.s_input,
        ]:
            layout.addWidget(w)

        layout.addLayout(button_layout)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

        # Connect signals
        self.run_button.clicked.connect(self.run_solver)
        self.open_button.clicked.connect(self.open_file)
        self.delete_button.clicked.connect(self.delete_file)

    def run_solver(self):
        try:
            m = int(self.m_input.text())
            n = int(self.n_input.text())
            k = int(self.k_input.text())
            j = int(self.j_input.text())
            s = int(self.s_input.text())

            self.result_area.setText("Running...\n")

            prob = Problem(m, n, k, j, s)
            solver = GreedySolver(prob)

            output = solver.solve()

            results = output["results"]
            count = output["count"]

            self.result_area.clear()
            self.result_area.append(f"Count: {count}")
            self.result_area.append(f"Time: {output['time']:.2f}s\n")

            for i, combo in enumerate(results):
                if i > 50:
                    self.result_area.append("... truncated ...")
                    break
                self.result_area.append(f"{i+1}. {','.join(map(str, combo))}")

            # Auto-save results to file
            try:
                file_path = self.save_results_to_file(
                    m, n, k, j, s, prob.samples, results, count
                )
                self.loaded_file_path = file_path
                self.status_label.setText(
                    f"Loaded: {os.path.basename(file_path)}"
                )
            except Exception as e:
                print(f"Failed to save results: {e}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def determine_next_run_id(self, m, n, k, j, s):
        """Scan results/ for files matching the parameter set and return
        the next RUN_ID (max existing + 1)."""
        pattern = re.compile(
            rf"^{re.escape(str(m))}-{re.escape(str(n))}-"
            rf"{re.escape(str(k))}-{re.escape(str(j))}-"
            rf"{re.escape(str(s))}-(\d+)-\d+\.txt$"
        )
        max_run_id = 0
        try:
            if not os.path.isdir(self.results_dir):
                return 1
            for fname in os.listdir(self.results_dir):
                m = pattern.match(fname)
                if m:
                    run_id = int(m.group(1))
                    if run_id > max_run_id:
                        max_run_id = run_id
        except OSError:
            pass
        return max_run_id + 1

    def save_results_to_file(self, m, n, k, j, s, samples, results, count):
        """Save results to a DB file in results/ and return the file path."""
        run_id = self.determine_next_run_id(m, n, k, j, s)
        os.makedirs(self.results_dir, exist_ok=True)
        file_name = f"{m}-{n}-{k}-{j}-{s}-{run_id}-{count}.txt"
        file_path = os.path.join(self.results_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Problem: m={m}, n={n}, k={k}, j={j}, s={s}\n")
            f.write(f"Samples: {samples}\n")
            f.write(f"Results Count: {count}\n")
            f.write("-" * 20 + "\n")
            for i, combo in enumerate(results, 1):
                f.write(f"{i}. {','.join(map(str, combo))}\n")

        return file_path

    def parse_result_file(self, file_path):
        """Parse a result file and return structured data, or None on error."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File not found:\n{file_path}")
            return None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")
            return None

        if not lines:
            QMessageBox.critical(self, "Error", "File is empty.")
            return None

        data = {"filename": os.path.basename(file_path)}

        # Parse header: "Problem: m=..., n=..., k=..., j=..., s=..."
        header_match = re.match(
            r"Problem:\s*m=(\d+),\s*n=(\d+),\s*k=(\d+),\s*j=(\d+),\s*s=(\d+)",
            lines[0]
        )
        if not header_match:
            QMessageBox.critical(self, "Error",
                                 "Corrupted file: invalid problem header.")
            return None

        data["m"] = int(header_match.group(1))
        data["n"] = int(header_match.group(2))
        data["k"] = int(header_match.group(3))
        data["j"] = int(header_match.group(4))
        data["s"] = int(header_match.group(5))

        # Parse samples: "Samples: [1, 2, 3, ...]"
        samples_match = re.match(r"Samples:\s*\[(.*?)\]", lines[1])
        if samples_match:
            sample_str = samples_match.group(1)
            data["samples"] = [
                int(x.strip()) for x in sample_str.split(",") if x.strip()
            ]
        else:
            data["samples"] = []

        # Parse count
        count_match = re.match(r"Results Count:\s*(\d+)", lines[2])
        data["count"] = int(count_match.group(1)) if count_match else 0

        # Parse result entries
        results = []
        for line in lines[4:]:
            line = line.strip()
            if not line:
                continue
            entry_match = re.match(r"\d+\.\s+(.*)", line)
            if entry_match:
                numbers = [
                    int(x.strip())
                    for x in entry_match.group(1).split(",")
                    if x.strip()
                ]
                results.append(numbers)

        data["results"] = results
        return data

    def open_file(self):
        """Open a result file dialog, parse and display results."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Result File", self.results_dir, "Result Files (*.txt)"
        )
        if not file_path:
            return

        data = self.parse_result_file(file_path)
        if data is None:
            return

        # Populate input fields with loaded parameters
        self.m_input.setText(str(data["m"]))
        self.n_input.setText(str(data["n"]))
        self.k_input.setText(str(data["k"]))
        self.j_input.setText(str(data["j"]))
        self.s_input.setText(str(data["s"]))

        # Display results
        self.result_area.clear()
        self.result_area.append(
            f"Problem: m={data['m']}, n={data['n']}, k={data['k']}, "
            f"j={data['j']}, s={data['s']}"
        )
        self.result_area.append(f"Samples: {data['samples']}")
        self.result_area.append(f"Results Count: {data['count']}")
        self.result_area.append("-" * 20)

        for i, combo in enumerate(data["results"]):
            if i > 50:
                self.result_area.append("... truncated ...")
                break
            self.result_area.append(f"{i+1}. {','.join(map(str, combo))}")

        self.loaded_file_path = file_path
        self.status_label.setText(f"Loaded: {data['filename']}")

    def delete_file(self):
        """Delete the currently loaded file after user confirmation."""
        if self.loaded_file_path is None:
            QMessageBox.warning(self, "Warning",
                                "No file is currently loaded.")
            return

        fname = os.path.basename(self.loaded_file_path)
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete:\n{fname}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            os.remove(self.loaded_file_path)
            self.loaded_file_path = None
            self.status_label.setText("Loaded: (none)")
            self.result_area.clear()
        except OSError as e:
            QMessageBox.critical(self, "Error", f"Cannot delete file:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())