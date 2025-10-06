import os
import sys
import traceback
import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext

class ShellEmulator:
    PROMPT_SUFFIX = "$ "

    def __init__(self, root, vfs_path=None, startup_script=None):
        self.root = root
        self.user = self._safe_get_user()
        self.host = self._safe_get_hostname()
        self.vfs_path = vfs_path
        self.startup_script = startup_script
        self.cwd = os.getcwd()  # Начальная директория

        # Настройка окна
        self.root.title(f"Эмулятор - [{self.user}@{self.host}]")
        self.root.geometry("800x500")

        # Виджеты
        self.output = scrolledtext.ScrolledText(root, state="disabled", wrap="word")
        self.output.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        entry_frame = tk.Frame(root)
        entry_frame.pack(fill=tk.X, padx=4, pady=(0, 4))

        self.entry = tk.Entry(entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self._on_enter)

        btn = tk.Button(entry_frame, text="Enter", command=self._on_enter)
        btn.pack(side=tk.RIGHT)

        # Отладочный вывод параметров
        self._write_line("=== Отладка параметров запуска ===")
        self._write_line(f"VFS Path: {self.vfs_path}")
        self._write_line(f"Startup Script: {self.startup_script}")
        self._write_line("=================================")

        self._write_line("Добро пожаловать в GUI-эмулятор шелла.")
        self._write_line("Введи 'help' для списка доступных команд.\n")
        self._print_prompt()

        # Если есть стартовый скрипт — выполняем его
        if self.startup_script:
            self._run_startup_script()

    def _safe_get_user(self):
        try:
            return getpass.getuser()
        except Exception:
            return os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"

    def _safe_get_hostname(self):
        try:
            return socket.gethostname()
        except Exception:
            return "localhost"

    def _write(self, text: str):
        self.output.config(state="normal")
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state="disabled")

    def _write_line(self, text: str = ""):
        self._write(str(text) + "\n")

    def _print_prompt(self):
        prompt = f"{self.user}@{self.host}:{self.cwd}{self.PROMPT_SUFFIX}"
        self._write(prompt)

    def _on_enter(self, event=None):
        raw = self.entry.get()
        self.entry.delete(0, tk.END)
        self._process_input(raw)

    def _process_input(self, raw: str):
        if not raw.strip():
            self._write_line("")
            self._print_prompt()
            return

        self._write_line(raw)
        parts = raw.strip().split()
        cmd = parts[0]
        args = parts[1:]

        try:
            self._execute_command(cmd, args)
        except Exception:
            self._write_line("Ошибка при выполнении команды:")
            self._write_line(traceback.format_exc())

        self._print_prompt()

    def _execute_command(self, cmd: str, args: list):
        commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
            "help": self.cmd_help
        }
        if cmd in commands:
            commands[cmd](args)
        else:
            self._write_line(f"Command not found: {cmd}")

    def cmd_ls(self, args):
        # Реализация заглушки
        self._write_line(f"[Заглушка] Выполнение команды 'ls' с аргументами: {args}")

    def cmd_cd(self, args):
        if not args:
            self._write_line("cd: путь не указан")
            return
        try:
            new_dir = args[0]
            os.chdir(new_dir)
            self.cwd = os.getcwd()
        except Exception as e:
            self._write_line(f"cd: {e}")

    def cmd_exit(self, args):
        self._write_line("Выход из эмулятора...")
        self.root.after(200, self.root.destroy)

    def cmd_help(self, args):
        self._write_line("Доступные команды:")
        self._write_line(" ls — заглушка для команды 'ls'")
        self._write_line(" cd — смена директории")
        self._write_line(" exit — завершить эмулятор")
        self._write_line(" help — показать это сообщение")

    def _run_startup_script(self):
        if not os.path.exists(self.startup_script):
            self._write_line(f"Стартовый скрипт не найден: {self.startup_script}")
            return
        self._write_line(f"\n=== Выполнение стартового скрипта: {self.startup_script} ===")
        try:
            with open(self.startup_script, "r", encoding="utf-8") as f:
                for line in f:
                    cmd_line = line.strip()
                    if not cmd_line or cmd_line.startswith("#"):
                        continue
                    try:
                        self._write_line(cmd_line)  # Эмуляция ввода
                        self._process_input(cmd_line)
                    except Exception:
                        self._write_line(f"Ошибка в строке: {cmd_line}")
                        continue
            self._write_line(f"=== Скрипт выполнен ===\n")
        except Exception as e:
            self._write_line(f"Ошибка при выполнении скрипта: {e}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="GUI Shell Emulator")
    parser.add_argument("--vfs", type=str, help="Путь к физическому расположению VFS")
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту")
    args = parser.parse_args()

    root = tk.Tk()
    app = ShellEmulator(root, vfs_path=args.vfs, startup_script=args.script)
    root.mainloop()

if __name__ == "__main__":
    main()
