import json
import os
import sys
import tkinter as tk
from tkinter import messagebox

# إذا كان البرنامج exe نحفظ البيانات جنب ملف الـ exe (وليس في مجلد مؤقت)
if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "tasks.json")
SETTINGS_FILE = os.path.join(BASE, "settings.json")


def resource_path(name):
    """مسار ملفات مضمّنة مع الـ exe (مثل الأيقونة)"""
    root = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, name)

# ---------- الثيمات ----------
THEMES = {
    "light": {"name": "فاتح", "BG": "#eef1f8", "CARD": "#ffffff", "HEADER": "#1e2a5a", "HEAD": "#1e2a5a",
              "PRIMARY": "#4263eb", "GREEN": "#2f9e44", "RED": "#e03131", "GRAY": "#868e96",
              "GRAY_L": "#f1f3f5", "BORDER": "#dfe3ee", "TEXT": "#212529"},
    "dark": {"name": "داكن", "BG": "#14161c", "CARD": "#1f232d", "HEADER": "#191c25", "HEAD": "#e9ecef",
             "PRIMARY": "#5c7cfa", "GREEN": "#37b24d", "RED": "#fa5252", "GRAY": "#9a9fa8",
             "GRAY_L": "#2b303b", "BORDER": "#313744", "TEXT": "#e9ecef"},
    "warm": {"name": "دافئ", "BG": "#f6efe6", "CARD": "#fffaf3", "HEADER": "#5b4636", "HEAD": "#5b4636",
             "PRIMARY": "#c2691f", "GREEN": "#5f8f3e", "RED": "#c0392b", "GRAY": "#8a7967",
             "GRAY_L": "#efe4d4", "BORDER": "#e2d3bf", "TEXT": "#3e2f23"},
    "nature": {"name": "طبيعي", "BG": "#eef4ee", "CARD": "#fbfdfb", "HEADER": "#2f5d3a", "HEAD": "#2f5d3a",
               "PRIMARY": "#2b8a7b", "GREEN": "#2f9e44", "RED": "#c92a2a", "GRAY": "#7b8a7d",
               "GRAY_L": "#e3ece4", "BORDER": "#d0ddd1", "TEXT": "#1f2d22"},
}

SETTINGS = {"theme": "light", "scale": 100}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                SETTINGS.update(json.load(f))
        except Exception:
            pass
    if SETTINGS["theme"] not in THEMES:
        SETTINGS["theme"] = "light"


def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(SETTINGS, f, ensure_ascii=False)


def F(size, bold=False):
    s = max(7, round(size * SETTINGS["scale"] / 100))
    return ("Tahoma", s, "bold") if bold else ("Tahoma", s)


def apply_style():
    """يحدّث الألوان والخطوط (متغيرات عامة) حسب الإعدادات"""
    t = THEMES[SETTINGS["theme"]]
    g = globals()
    for k, v in t.items():
        if k != "name":
            g[k] = v
    g["FONT"] = F(12)
    g["FONT_S"] = F(10)
    g["FONT_B"] = F(12, True)
    g["FONT_T"] = F(17, True)


apply_style()


# ---------- التخزين ----------
def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


# ---------- عناصر مساعدة ----------
class Btn(tk.Label):
    """زر مخصص يشتغل بالألوان على كل الأنظمة"""
    def __init__(self, master, text, command, bg=None, fg="white", font=None, **kw):
        super().__init__(master, text=text, bg=bg or PRIMARY, fg=fg, font=font or FONT_B,
                         padx=16, pady=7, cursor="hand2", **kw)
        self._cmd = command
        self.bind("<Button-1>", lambda e: self._cmd())

    def set(self, text, bg, fg="white"):
        self.config(text=text, bg=bg, fg=fg)


class PEntry(tk.Entry):
    """خانة كتابة فيها نص إرشادي رمادي، و get() ترجع فراغ إذا ما كتب شي"""
    def __init__(self, master, hint="", **kw):
        super().__init__(master, font=FONT, justify="right", relief="flat", bd=0,
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=PRIMARY, bg=CARD, fg=TEXT, insertbackground=TEXT, **kw)
        self.hint = hint
        self.empty = False
        self.bind("<FocusIn>", self._in)
        self.bind("<FocusOut>", self._out)
        self._show_hint()

    def _show_hint(self):
        if not super().get():
            self.empty = True
            self.config(fg=GRAY)
            super().insert(0, self.hint)

    def _in(self, e=None):
        if self.empty:
            super().delete(0, "end")
            self.config(fg=TEXT)
            self.empty = False

    def _out(self, e=None):
        if not super().get():
            self._show_hint()

    def get(self):
        return "" if self.empty else super().get().strip()

    def put(self, text):
        self._in()
        super().delete(0, "end")
        if text:
            super().insert(0, text)
        else:
            self._show_hint()


class Scroll(tk.Frame):
    def __init__(self, master, bg=None):
        bg = bg or BG
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.win, width=e.width))
        self.canvas.configure(yscrollcommand=sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._wheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _wheel(self, e):
        try:
            self.canvas.yview_scroll(-1 if e.delta > 0 else 1, "units")
        except tk.TclError:
            pass


def card(parent, **kw):
    return tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1, **kw)


def header_bar(parent):
    bar = tk.Frame(parent, bg=HEADER)
    bar.pack(fill="x")
    return bar


# ---------- نافذة الإعدادات ----------
class SettingsWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("الإعدادات")
        self.geometry("460x520")
        self.build()

    def build(self):
        for w in self.winfo_children():
            w.destroy()
        self.configure(bg=BG)

        bar = header_bar(self)
        Btn(bar, "✕ إغلاق", self.destroy, bg=RED, font=FONT_S).pack(side="left", padx=12, pady=10)
        tk.Label(bar, text="⚙ الإعدادات", bg=HEADER, fg="white", font=FONT_B).pack(side="right", padx=16)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=16)

        # الألوان
        tk.Label(body, text="نمط الألوان", bg=BG, fg=HEAD, font=FONT_B).pack(anchor="e", pady=(0, 8))
        grid = tk.Frame(body, bg=BG)
        grid.pack(fill="x")
        grid.grid_columnconfigure(0, weight=1, uniform="a")
        grid.grid_columnconfigure(1, weight=1, uniform="a")
        for i, (key, t) in enumerate(THEMES.items()):
            selected = key == SETTINGS["theme"]
            box = tk.Frame(grid, bg=t["BG"], cursor="hand2", highlightthickness=3,
                           highlightbackground=PRIMARY if selected else BORDER)
            box.grid(row=i // 2, column=1 - (i % 2), padx=6, pady=6, sticky="nsew")
            top = tk.Frame(box, bg=t["HEADER"], height=16)
            top.pack(fill="x")
            mid = tk.Frame(box, bg=t["BG"])
            mid.pack(fill="x", padx=10, pady=8)
            tk.Frame(mid, bg=t["PRIMARY"], width=14, height=14).pack(side="right", padx=2)
            tk.Frame(mid, bg=t["GREEN"], width=14, height=14).pack(side="right", padx=2)
            lbl = tk.Label(box, text=("✔ " if selected else "") + t["name"], bg=t["BG"],
                           fg=t["TEXT"], font=FONT_B)
            lbl.pack(pady=(0, 8))
            for w in (box, top, mid, lbl) + tuple(mid.winfo_children()):
                w.bind("<Button-1>", lambda e, k=key: self.app.change(theme=k))

        # حجم الخط
        tk.Label(body, text="حجم الخط والعناصر", bg=BG, fg=HEAD, font=FONT_B).pack(anchor="e", pady=(18, 6))
        c = card(body)
        c.pack(fill="x")
        self.pct = tk.Label(c, text=f"{SETTINGS['scale']}%", bg=CARD, fg=PRIMARY, font=FONT_B)
        self.pct.pack(pady=(10, 0))
        sc = tk.Scale(c, from_=80, to=150, resolution=5, orient="horizontal", showvalue=False,
                      bg=CARD, troughcolor=GRAY_L, highlightthickness=0, bd=0,
                      activebackground=PRIMARY, length=300,
                      command=lambda v: self.pct.config(text=f"{v}%"))
        sc.set(SETTINGS["scale"])
        sc.pack(padx=16, pady=4)
        sc.bind("<ButtonRelease-1>", lambda e: self.app.change(scale=sc.get()))
        sc.bind("<KeyRelease>", lambda e: self.app.change(scale=sc.get()))
        tk.Label(c, text="اسحب الشريط لتكبير أو تصغير الخط", bg=CARD, fg=GRAY, font=FONT_S).pack(pady=(0, 6))
        tk.Label(c, text="هذا مثال على شكل الخط", bg=CARD, fg=TEXT, font=FONT).pack(pady=(0, 12))

        tk.Label(body, text="ملاحظة: عند التغيير تنقفل نوافذ المهام المفتوحة.", bg=BG, fg=GRAY,
                 font=FONT_S).pack(anchor="e", pady=(14, 0))


# ---------- نافذة إنشاء مهمة ----------
class CreateWindow(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.title("إنشاء مهمة")
        self.geometry("480x660")
        self.configure(bg=BG)
        self.transient(app.root)
        self.grab_set()
        self.day_entries = []

        bar = header_bar(self)
        Btn(bar, "✕ إغلاق", self.destroy, bg=RED, font=FONT_S).pack(side="left", padx=12, pady=10)
        tk.Label(bar, text="مهمة جديدة", bg=HEADER, fg="white", font=FONT_B).pack(side="right", padx=16)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=(14, 0))

        tk.Label(body, text="1- اسم المهمة", bg=BG, font=FONT_B, fg=TEXT).pack(anchor="e", pady=(0, 4))
        self.name = PEntry(body, hint="مثال: مراجعة الرياضيات")
        self.name.pack(fill="x", ipady=8)

        tk.Label(body, text="2- عدد الأيام", bg=BG, font=FONT_B, fg=TEXT).pack(anchor="e", pady=(14, 4))
        self.days = tk.Spinbox(body, from_=1, to=60, font=FONT, justify="center", relief="flat",
                               bg=CARD, fg=TEXT, insertbackground=TEXT, buttonbackground=GRAY_L,
                               highlightthickness=1, highlightbackground=BORDER,
                               highlightcolor=PRIMARY, command=self.build_days)
        self.days.delete(0, "end")
        self.days.insert(0, "3")
        self.days.pack(fill="x", ipady=8)
        self.days.bind("<KeyRelease>", lambda e: self.build_days())

        tk.Label(body, text="3- وش تسوي في كل يوم؟ (اختياري)", bg=BG, font=FONT_B,
                 fg=TEXT).pack(anchor="e", pady=(14, 4))
        self.scroll = Scroll(body)
        self.scroll.pack(fill="both", expand=True)

        bottom = tk.Frame(self, bg=BG)
        bottom.pack(fill="x", padx=18, pady=14)
        Btn(bottom, "إنشاء", self.create, bg=GREEN, font=F(13, True)).pack(fill="x")

        self.build_days()

    def build_days(self):
        try:
            n = max(1, min(60, int(self.days.get())))
        except ValueError:
            return
        old = [e.get() for e in self.day_entries]
        for w in self.scroll.inner.winfo_children():
            w.destroy()
        self.day_entries = []
        for i in range(n):
            row = tk.Frame(self.scroll.inner, bg=BG)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"اليوم {i + 1}", bg=BG, font=FONT, width=8, anchor="e",
                     fg=HEAD).pack(side="right")
            e = PEntry(row, hint="فاضي")
            e.pack(side="right", fill="x", expand=True, ipady=6, padx=(0, 6))
            if i < len(old) and old[i]:
                e.put(old[i])
            self.day_entries.append(e)

    def create(self):
        name = self.name.get()
        if not name:
            messagebox.showwarning("تنبيه", "اكتب اسم المهمة", parent=self)
            return
        try:
            n = int(self.days.get())
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("تنبيه", "عدد الأيام غير صحيح", parent=self)
            return
        self.build_days()
        self.app.tasks.append({
            "name": name,
            "days": [{"todo": e.get(), "done": False} for e in self.day_entries],
        })
        save_tasks(self.app.tasks)
        self.app.refresh()
        self.destroy()


# ---------- نافذة تفاصيل المهمة ----------
class TaskWindow(tk.Toplevel):
    def __init__(self, app, task):
        super().__init__(app.root)
        self.app = app
        self.task = task
        self.title(task["name"])
        self.geometry("700x700")
        self.configure(bg=BG)
        self.remaining = 0
        self.running = False
        self.job = None

        bar = header_bar(self)
        tk.Label(bar, text=task["name"], bg=HEADER, fg="white", font=FONT_T).pack(pady=12)

        # ----- التايمر يمين / الأيام المتبقية يسار -----
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=14, pady=14)

        tcard = card(top)
        tcard.pack(side="right", fill="y")
        tk.Label(tcard, text="⏱ التايمر", bg=CARD, font=FONT_B, fg=HEAD).pack(anchor="e", padx=16, pady=(10, 4))

        inputs = tk.Frame(tcard, bg=CARD)
        inputs.pack(padx=16)
        self.h_var = tk.StringVar()
        self.m_var = tk.StringVar()
        vcmd = (self.register(lambda s: s == "" or (s.isdigit() and len(s) <= 3)), "%P")

        def timer_entry(var, col):
            e = tk.Entry(inputs, textvariable=var, width=5, font=FONT_B, justify="center", relief="flat",
                         bg=CARD, fg=TEXT, insertbackground=TEXT, highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=PRIMARY,
                         validate="key", validatecommand=vcmd)
            e.grid(row=0, column=col, padx=4, ipady=5)

        tk.Label(inputs, text="ساعة", bg=CARD, font=FONT_S, fg=GRAY).grid(row=0, column=3, padx=2)
        timer_entry(self.h_var, 2)
        tk.Label(inputs, text="دقيقة", bg=CARD, font=FONT_S, fg=GRAY).grid(row=0, column=1, padx=2)
        timer_entry(self.m_var, 0)
        self.h_var.trace_add("write", lambda *a: self.on_edit())
        self.m_var.trace_add("write", lambda *a: self.on_edit())

        self.clock = tk.Label(tcard, text="00:00:00", bg=CARD, fg=PRIMARY, font=F(26, True))
        self.clock.pack(padx=16, pady=6)
        btns = tk.Frame(tcard, bg=CARD)
        btns.pack(pady=(0, 12))
        self.start_btn = Btn(btns, "ابدأ", self.toggle, bg=GREEN)
        self.start_btn.pack(side="right", padx=4)
        Btn(btns, "إعادة", self.reset, bg=GRAY).pack(side="right", padx=4)

        lcard = card(top)
        lcard.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(lcard, text="المتبقي", bg=CARD, fg=GRAY, font=FONT_S).pack(pady=(14, 0))
        self.left_num = tk.Label(lcard, bg=CARD, fg=HEAD, font=F(36, True))
        self.left_num.pack()
        self.left_txt = tk.Label(lcard, bg=CARD, fg=GRAY, font=FONT)
        self.left_txt.pack(pady=(0, 14))

        # ----- الجدول -----
        head = tk.Frame(self, bg=PRIMARY)
        head.pack(fill="x", padx=14)
        head.grid_columnconfigure(1, weight=1)
        tk.Label(head, text="الحالة", bg=PRIMARY, fg="white", font=FONT_B, width=13).grid(row=0, column=0, pady=7)
        tk.Label(head, text="المطلوب", bg=PRIMARY, fg="white", font=FONT_B, anchor="e").grid(
            row=0, column=1, sticky="ew", padx=8)
        tk.Label(head, text="اليوم", bg=PRIMARY, fg="white", font=FONT_B, width=8).grid(row=0, column=2)

        self.scroll = Scroll(self)
        self.scroll.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.btns = []
        self.entries = []
        self.build_rows()
        self.update_left()
        self.reset()

    def destroy(self):
        if self.job:
            try:
                self.after_cancel(self.job)
            except Exception:
                pass
            self.job = None
        self.running = False
        super().destroy()

    # ----- الصفوف -----
    def build_rows(self):
        for i, d in enumerate(self.task["days"]):
            row = card(self.scroll.inner)
            row.pack(fill="x", pady=3)
            row.grid_columnconfigure(1, weight=1)
            b = Btn(row, "", lambda i=i: self.toggle_day(i), width=11)
            b.grid(row=0, column=0, padx=10, pady=9)
            e = PEntry(row, hint="اضغط واكتب المطلوب...")
            e.put(d["todo"])
            e.grid(row=0, column=1, sticky="ew", padx=6, ipady=6)
            e.bind("<KeyRelease>", lambda ev, i=i: self.save_todo(i), add="+")
            e.bind("<FocusOut>", lambda ev, i=i: self.save_todo(i), add="+")
            tk.Label(row, text=f"اليوم {i + 1}", bg=CARD, font=FONT_B, fg=HEAD, width=8).grid(
                row=0, column=2, padx=6)
            self.btns.append(b)
            self.entries.append(e)
            self.style_row(i)

    def save_todo(self, i):
        self.task["days"][i]["todo"] = self.entries[i].get()
        save_tasks(self.app.tasks)

    def style_row(self, i):
        if self.task["days"][i]["done"]:
            self.btns[i].set("✔ مكتمل", GREEN)
        else:
            self.btns[i].set("إكمال المهمة", GRAY_L, fg=TEXT)

    def toggle_day(self, i):
        d = self.task["days"][i]
        d["done"] = not d["done"]
        save_tasks(self.app.tasks)
        self.style_row(i)
        self.update_left()
        self.app.refresh()

    def update_left(self):
        left = sum(1 for d in self.task["days"] if not d["done"])
        if left == 0:
            self.left_num.config(text="🎉", fg=GREEN)
            self.left_txt.config(text="خلصت المهمة!")
        else:
            self.left_num.config(text=str(left), fg=HEAD)
            self.left_txt.config(text="يوم باقي")

    # ----- التايمر -----
    def fmt(self, s):
        return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"

    def read_seconds(self):
        return int(self.h_var.get() or 0) * 3600 + int(self.m_var.get() or 0) * 60

    def on_edit(self):
        if not self.running:
            self.reset()

    def reset(self):
        self.running = False
        if self.job:
            self.after_cancel(self.job)
            self.job = None
        self.remaining = self.read_seconds()
        self.clock.config(text=self.fmt(self.remaining))
        self.start_btn.set("ابدأ", GREEN)

    def toggle(self):
        if self.running:
            self.running = False
            if self.job:
                self.after_cancel(self.job)
                self.job = None
            self.start_btn.set("استمرار", GREEN)
            return
        if self.remaining <= 0:
            self.remaining = self.read_seconds()
        if self.remaining <= 0:
            messagebox.showinfo("التايمر", "حط الساعات أو الدقائق أول", parent=self)
            return
        self.running = True
        self.start_btn.set("إيقاف", RED)
        self.tick()

    def tick(self):
        if not self.running:
            return
        if self.remaining <= 0:
            self.running = False
            self.start_btn.set("ابدأ", GREEN)
            self.bell()
            messagebox.showinfo("انتهى الوقت", "خلص وقت التايمر 👏", parent=self)
            return
        self.remaining -= 1
        self.clock.config(text=self.fmt(self.remaining))
        self.job = self.after(1000, self.tick)


# ---------- الواجهة الرئيسية ----------
class App:
    def __init__(self):
        load_settings()
        apply_style()
        self.root = tk.Tk()
        self.root.title("مهامي الدراسية")
        self.set_icon()
        self.root.geometry("560x700")
        self.tasks = load_tasks()
        self.settings_win = None
        self.build()

    def set_icon(self):
        try:
            if sys.platform.startswith("win"):
                self.root.iconbitmap(default=resource_path("icon.ico"))
            else:
                self._icon = tk.PhotoImage(file=resource_path("icon.png"))
                self.root.iconphoto(True, self._icon)
        except Exception:
            pass

    def build(self):
        for w in self.root.winfo_children():
            if not isinstance(w, tk.Toplevel):
                w.destroy()
        self.root.configure(bg=BG)

        bar = header_bar(self.root)
        Btn(bar, "＋ إنشاء مهمة", lambda: CreateWindow(self)).pack(side="right", padx=14, pady=12)
        Btn(bar, "⚙", self.open_settings, bg=GRAY_L, fg=TEXT).pack(side="left", padx=14, pady=12)
        tk.Label(bar, text="📚 مهامي الدراسية", bg=HEADER, fg="white", font=FONT_T).pack(expand=True)

        self.scroll = Scroll(self.root)
        self.scroll.pack(fill="both", expand=True, padx=16, pady=14)
        self.refresh()

    def open_settings(self):
        if self.settings_win is not None and self.settings_win.winfo_exists():
            self.settings_win.lift()
            return
        self.settings_win = SettingsWindow(self)

    def change(self, theme=None, scale=None):
        if theme is not None:
            SETTINGS["theme"] = theme
        if scale is not None:
            if scale == SETTINGS["scale"] and theme is None:
                return
            SETTINGS["scale"] = int(scale)
        save_settings()
        apply_style()
        for w in self.root.winfo_children():
            if isinstance(w, tk.Toplevel) and w is not self.settings_win:
                w.destroy()
        self.build()
        if self.settings_win is not None and self.settings_win.winfo_exists():
            self.settings_win.build()

    def refresh(self):
        for w in self.scroll.inner.winfo_children():
            w.destroy()
        if not self.tasks:
            tk.Label(self.scroll.inner, text="لا يوجد", bg=BG, fg=GRAY, font=F(20)).pack(pady=170)
            return
        for t in self.tasks:
            done = sum(1 for d in t["days"] if d["done"])
            total = len(t["days"])
            wrap = tk.Frame(self.scroll.inner, bg=BG)
            wrap.pack(fill="x", pady=7)
            c = card(wrap)
            c.pack(fill="x")
            tk.Frame(c, bg=GREEN if done == total else PRIMARY, width=6).pack(side="right", fill="y")
            inner = tk.Frame(c, bg=CARD)
            inner.pack(fill="both", expand=True)

            tk.Label(inner, text=t["name"], bg=CARD, font=FONT_T, fg=HEAD,
                     anchor="e").pack(fill="x", padx=16, pady=(12, 0))
            status = "✔ مكتملة" if done == total else f"أُنجز {done} من {total} يوم"
            tk.Label(inner, text=status, bg=CARD, font=FONT, fg=GREEN if done == total else GRAY,
                     anchor="e").pack(fill="x", padx=16)
            pb = tk.Frame(inner, bg=GRAY_L, height=8)
            pb.pack(fill="x", padx=16, pady=10)
            pb.pack_propagate(False)
            if done:
                tk.Frame(pb, bg=GREEN).place(relx=1.0, rely=0, relwidth=done / total,
                                             relheight=1, anchor="ne")
            row = tk.Frame(inner, bg=CARD)
            row.pack(fill="x", padx=16, pady=(0, 12))
            Btn(row, "العمل على المهمة", lambda t=t: TaskWindow(self, t)).pack(side="right")
            Btn(row, "حذف", lambda t=t: self.delete(t), bg=GRAY_L, fg=RED).pack(side="left")

    def delete(self, task):
        if messagebox.askyesno("حذف", f"تحذف مهمة «{task['name']}»؟"):
            self.tasks.remove(task)
            save_tasks(self.tasks)
            self.refresh()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
