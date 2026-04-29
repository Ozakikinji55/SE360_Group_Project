import sys
import os
import re
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, 
    QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QFileDialog,
    QStackedWidget, QRadioButton, QButtonGroup, QListWidget, QFrame
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

            # 保存[cite: 4]
            run_id = self.get_next_run_id(m, n, k, j, s)
            file_name = f"{m}-{n}-{k}-{j}-{s}-{run_id}-{output['count']}.txt"
            file_path = os.path.join(self.results_dir, file_name)
            with open(file_path, "w") as f:
                f.write(f"Problem: m={m}, n={n}, k={k}, j={j}, s={s}\nSamples: {prob.samples}\nResults Count: {output['count']}\n" + "-"*20 + "\n")
                for i, combo in enumerate(output['results'], 1):
                    f.write(f"{i}. {combo}\n")
            
            QMessageBox.information(self, "Success", f"Results saved to {file_name}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置全应用样式提升观感
    app.setStyleSheet("QPushButton { height: 30px; } QLineEdit { height: 25px; }")
    window = App()
    window.show()
    sys.exit(app.exec_())