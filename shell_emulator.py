import os
import sys
import traceback
import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext

class ShellEmulator:
    PROMPT_SUFFIX = "$ "

    def __init__(self, root):
        self.root = root
        self.user = self._safe_get_user()
        self.host = self._safe_get_hostname()
        self.cwd = os.getcwd()

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

        self._write_line("Добро пожаловать в GUI-эмулятор шелла.")
        self._write_line("Введи 'help' для списка доступных команд.\n")
        self._print_prompt()

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
        self._write_line(f"[Заглушка] Выполнение команды 'ls' с аргументами: {args}")

    def cmd_cd(self, args):
        self._write_line(f"[Заглушка] Выполнение команды 'cd' с аргументами: {args}")

    def cmd_exit(self, args):
        self._write_line("Выход из эмулятора...")
        self.root.after(200, self.root.destroy)

    def cmd_help(self, args):
        self._write_line("Доступные команды:")
        self._write_line(" ls — заглушка для команды 'ls'")
        self._write_line(" cd — заглушка для команды 'cd'")
        self._write_line(" exit — завершить эмулятор")
        self._write_line(" help — показать это сообщение")

def main():
    root = tk.Tk()
    app = ShellEmulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
