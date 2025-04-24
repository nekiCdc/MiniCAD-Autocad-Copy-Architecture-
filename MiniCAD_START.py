import tkinter as tk
import math

class MiniCAD:
    def __init__(self, root):
        self.root = root
        self.root.title("CoddyCODE MiniCAD")
        self.root.geometry("900x700")
        self.command = ""
        self.theme = "dark"
        self.start_point = None
        self.preview = None

        self.init_colors()
        self.create_ui()
        self.draw_grid()

    def init_colors(self):
        if self.theme == "dark":
            self.bg = "#1e1e1e"
            self.fg = "#ffffff"
            self.grid_color = "#444"
            self.line_color = "#ffffff"
        else:
            self.bg = "#ffffff"
            self.fg = "#000000"
            self.grid_color = "#ccc"
            self.line_color = "#000000"

    def create_ui(self):
        self.command_frame = tk.Frame(self.root, bg=self.bg)
        self.command_frame.pack(fill="x", side="top")

        self.command_entry = tk.Entry(self.command_frame, bg=self.bg, fg=self.fg, font=("Consolas", 14))
        self.command_entry.pack(fill="x", padx=10, pady=5)
        self.command_entry.bind("<Return>", self.handle_command)

        self.hint_label = tk.Label(self.command_frame, text="Команды: L, LN, REC, TR, THEME, ESC", bg=self.bg, fg=self.fg)
        self.hint_label.pack(anchor="w", padx=10)

        # Кнопка "Enter" для сохранения линии
        self.enter_button = tk.Button(self.command_frame, text="Enter", command=self.save_line, bg=self.bg, fg=self.fg)
        self.enter_button.pack(padx=10, pady=5)

        self.canvas = tk.Canvas(self.root, bg=self.bg, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.preview_draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        self.canvas.bind("<Motion>", self.update_cursor)

        self.distance_text = self.canvas.create_text(5, 5, text="", anchor="nw", fill="red", font=("Consolas", 10))

    def draw_grid(self):
        self.canvas.delete("grid")
        for i in range(0, 2000, 20):
            self.canvas.create_line(i, 0, i, 2000, fill=self.grid_color, tags="grid")
            self.canvas.create_line(0, i, 2000, i, fill=self.grid_color, tags="grid")

    def handle_command(self, event):
        cmd = self.command_entry.get().strip().upper()
        if cmd == "THEME":
            self.theme = "light" if self.theme == "dark" else "dark"
            self.init_colors()
            self.canvas.config(bg=self.bg)
            self.command_frame.config(bg=self.bg)
            self.hint_label.config(bg=self.bg, fg=self.fg)
            self.command_entry.config(bg=self.bg, fg=self.fg)
            self.draw_grid()
        elif cmd == "ESC":
            self.command = ""
            self.start_point = None
            self.canvas.delete("preview")
        else:
            self.command = cmd
        self.command_entry.delete(0, tk.END)

    def start_draw(self, event):
        if self.command in ["L", "LN", "REC"]:
            self.start_point = (event.x, event.y)

    def preview_draw(self, event):
        if not self.start_point or self.command not in ["L", "LN", "REC"]:
            return

        self.canvas.delete("preview")
        x0, y0 = self.start_point
        x1, y1 = event.x, event.y

        if self.command == "L":
            if abs(x1 - x0) > abs(y1 - y0):
                y1 = y0
            else:
                x1 = x0
            self.preview = self.canvas.create_line(x0, y0, x1, y1, fill="red", tags="preview", width=2)
        elif self.command == "LN":
            self.preview = self.canvas.create_line(x0, y0, x1, y1, fill="red", tags="preview", width=2)
        elif self.command == "REC":
            self.preview = self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="preview", width=2)

        dist = round(math.hypot(x1 - x0, y1 - y0) / 10, 1)
        self.canvas.coords(self.distance_text, x1 + 5, y1 + 5)
        self.canvas.itemconfig(self.distance_text, text=f"{dist} см")

    def end_draw(self, event):
        if not self.start_point:
            return
        x0, y0 = self.start_point
        x1, y1 = event.x, event.y
        self.canvas.delete("preview")

        if self.command == "L":
            if abs(x1 - x0) > abs(y1 - y0):
                y1 = y0
            else:
                x1 = x0
            self.canvas.create_line(x0, y0, x1, y1, fill=self.line_color, width=2, tags="line")
        elif self.command == "LN":
            self.canvas.create_line(x0, y0, x1, y1, fill=self.line_color, width=2, tags="line")
        elif self.command == "REC":
            self.canvas.create_rectangle(x0, y0, x1, y1, outline=self.line_color, width=2, tags="line")

        self.start_point = None
        self.canvas.itemconfig(self.distance_text, text="")

    def update_cursor(self, event):
        self.canvas.delete("cursor")
        size = 100  # размер курсора
        self.canvas.create_line(event.x - size, event.y, event.x + size, event.y, fill="cyan", tags="cursor")
        self.canvas.create_line(event.x, event.y - size, event.x, event.y + size, fill="cyan", tags="cursor")

    def save_line(self):
        # Сохранение линии на холсте при нажатии на кнопку Enter
        if self.start_point and self.command in ["L", "LN", "REC"]:
            x0, y0 = self.start_point
            x1, y1 = self.canvas.coords(self.preview)[:2]
            if self.command == "L":
                if abs(x1 - x0) > abs(y1 - y0):
                    y1 = y0
                else:
                    x1 = x0
                self.canvas.create_line(x0, y0, x1, y1, fill=self.line_color, width=2, tags="line")
            elif self.command == "LN":
                self.canvas.create_line(x0, y0, x1, y1, fill=self.line_color, width=2, tags="line")
            elif self.command == "REC":
                self.canvas.create_rectangle(x0, y0, x1, y1, outline=self.line_color, width=2, tags="line")
            self.canvas.delete("preview")  # Удаление превью
            self.start_point = None

root = tk.Tk()
app = MiniCAD(root)
root.mainloop()