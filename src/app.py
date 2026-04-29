import sys
import os
<<<<<<< HEAD
import re
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, 
    QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QFileDialog,
    QStackedWidget, QRadioButton, QButtonGroup, QListWidget, QFrame
=======
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
>>>>>>> d8ddfd304001b79a0809f62d72e64b01bdc171d6
)
from PyQt5.QtCore import Qt

# 导入你的核心逻辑
from core.problem import Problem
from solvers.ilp_solver import ILPSolver
from solvers.greedy_solver import GreedySolver
from solvers.meta_solver import MetaSolver

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("An Optimal Samples Selection System")
        self.setGeometry(100, 100, 600, 750)
        
        self.results_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "results"))
        os.makedirs(self.results_dir, exist_ok=True)

<<<<<<< HEAD
        # 使用堆叠布局实现双页面切换
        self.stack = QStackedWidget()
        self.init_input_page()      # 页面 0：参数输入
        self.init_database_page()   # 页面 1：历史查看
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def init_input_page(self):
        """页面 1: 参数输入与执行"""
        page = QWidget()
        layout = QVBoxLayout()
        
        title = QLabel("An Optimal Samples Selection System")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- 参数输入区域 ---
        form_layout = QVBoxLayout()
        self.inputs = {}
        params = [
            ("m", "45", "45 ≤ m ≤ 54"),
            ("n", "12", "7 ≤ n ≤ 25"),
            ("k", "6", "4 ≤ k ≤ 7"),
            ("j", "5", "s ≤ j ≤ k"),
            ("s", "5", "3 ≤ s ≤ 7")
        ]
        for label, default, hint in params:
            h_box = QHBoxLayout()
            lbl = QLabel(f"{label}:")
            lbl.setFixedWidth(30)
            edit = QLineEdit(default)
            hint_lbl = QLabel(hint)
            hint_lbl.setStyleSheet("color: gray; font-size: 11px;")
            h_box.addWidget(lbl)
            h_box.addWidget(edit)
            h_box.addWidget(hint_lbl)
            self.inputs[label] = edit
            form_layout.addLayout(h_box)
        layout.addLayout(form_layout)

        # --- 样本选择模式 ---
        mode_box = QHBoxLayout()
        self.radio_random = QRadioButton("Random n")
        self.radio_manual = QRadioButton("Input n")
        self.radio_random.setChecked(True)
        mode_box.addWidget(self.radio_random)
        mode_box.addWidget(self.radio_manual)
        self.manual_input = QLineEdit()
        self.manual_input.setPlaceholderText("e.g. 1,2,3... (only for Input n mode)")
        layout.addLayout(mode_box)
        layout.addWidget(self.manual_input)

        # --- 按钮区 ---
        btn_layout = QHBoxLayout()
        self.run_btn = QPushButton("EXECUTE")
        self.clear_btn = QPushButton("CLEAR")
        self.next_btn = QPushButton("DATABASE NEXT >")
        
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.next_btn)
        layout.addLayout(btn_layout)

        # --- 结果显示 ---
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(QLabel("Result Preview:"))
        layout.addWidget(self.result_display)

        # 事件绑定
        self.run_btn.clicked.connect(self.run_solver)
        self.clear_btn.clicked.connect(self.clear_inputs)
        self.next_btn.clicked.connect(lambda: (self.refresh_db_list(), self.stack.setCurrentIndex(1)))
        
        page.setLayout(layout)
        self.stack.addWidget(page)

    def init_database_page(self):
        """页面 2: 数据库历史文件管理"""
        page = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Data Base Resource Display (DB file)"))
        
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        self.db_content_view = QTextEdit()
        self.db_content_view.setReadOnly(True)
        layout.addWidget(QLabel("File Detail:"))
        layout.addWidget(self.db_content_view)

        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("< BACK")
        self.delete_btn = QPushButton("DELETE")
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        # 事件绑定
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.file_list.itemClicked.connect(self.load_db_file)
        self.delete_btn.clicked.connect(self.delete_file)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # --- 功能实现 ---
    def clear_inputs(self):
        for edit in self.inputs.values(): edit.clear()
        self.manual_input.clear()
        self.result_display.clear()
=======
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
>>>>>>> d8ddfd304001b79a0809f62d72e64b01bdc171d6

    def run_solver(self):
        try:
            m = int(self.inputs['m'].text())
            n = int(self.inputs['n'].text())
            k = int(self.inputs['k'].text())
            j = int(self.inputs['j'].text())
            s = int(self.inputs['s'].text())

            # 处理样本输入模式
            if self.radio_manual.isChecked():
                user_samples = [int(x.strip()) for x in self.manual_input.text().split(",") if x.strip()]
                if len(user_samples) != n:
                    raise ValueError(f"Please input exactly {n} samples.")
                prob = Problem(m, n, k, j, s)
                prob.samples = sorted(user_samples)
            else:
                prob = Problem(m, n, k, j, s)

            # 修正算法选择逻辑[cite: 2, 3]
            if n <= 12: solver = ILPSolver(prob)
            elif n <= 20: solver = GreedySolver(prob)
            else: solver = MetaSolver(prob)

            self.result_display.setText("Calculating... Please wait.")
            QApplication.processEvents() # 刷新界面显示

            output = solver.solve()
            
            # 显示结果
            self.result_display.clear()
            self.result_display.append(f"Samples Selected: {prob.samples}")
            self.result_display.append(f"Result Count: {output['count']}")
            self.result_display.append(f"Time: {output['time']:.2f}s\n")
            for i, combo in enumerate(output['results'][:10]):
                self.result_display.append(f"{i+1}. {combo}")

<<<<<<< HEAD
            # 保存[cite: 4]
            run_id = self.get_next_run_id(m, n, k, j, s)
            file_name = f"{m}-{n}-{k}-{j}-{s}-{run_id}-{output['count']}.txt"
            file_path = os.path.join(self.results_dir, file_name)
            with open(file_path, "w") as f:
                f.write(f"Problem: m={m}, n={n}, k={k}, j={j}, s={s}\nSamples: {prob.samples}\nResults Count: {output['count']}\n" + "-"*20 + "\n")
                for i, combo in enumerate(output['results'], 1):
                    f.write(f"{i}. {combo}\n")
            
            QMessageBox.information(self, "Success", f"Results saved to {file_name}")
=======
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
>>>>>>> d8ddfd304001b79a0809f62d72e64b01bdc171d6

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

<<<<<<< HEAD
    def get_next_run_id(self, m, n, k, j, s):
        pattern = re.compile(rf"^{m}-{n}-{k}-{j}-{s}-(\d+)-.*\.txt$")
        max_id = 0
        for f in os.listdir(self.results_dir):
            match = pattern.match(f)
            if match: max_id = max(max_id, int(match.group(1)))
        return max_id + 1

    def refresh_db_list(self):
        self.file_list.clear()
        if os.path.exists(self.results_dir):
            files = [f for f in os.listdir(self.results_dir) if f.endswith(".txt")]
            self.file_list.addItems(sorted(files, reverse=True))

    def load_db_file(self, item):
        file_path = os.path.join(self.results_dir, item.text())
        with open(file_path, "r") as f:
            self.db_content_view.setText(f.read())

    def delete_file(self):
        item = self.file_list.currentItem()
        if not item: return
        if QMessageBox.question(self, "Delete", f"Delete {item.text()}?") == QMessageBox.Yes:
            os.remove(os.path.join(self.results_dir, item.text()))
            self.refresh_db_list()
            self.db_content_view.clear()
=======
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

>>>>>>> d8ddfd304001b79a0809f62d72e64b01bdc171d6

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置全应用样式提升观感
    app.setStyleSheet("QPushButton { height: 30px; } QLineEdit { height: 25px; }")
    window = App()
    window.show()
    sys.exit(app.exec_())