"""مهامي الدراسية - واجهة Qt (PySide6 أو PyQt6) بنافذة واحدة وصفحات داخلها"""
import json
import math
import os
import random
import sys
import time

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PyQt6 import QtCore, QtGui, QtWidgets
for _m in (QtCore, QtGui, QtWidgets):
    globals().update({k: getattr(_m, k) for k in dir(_m) if k.startswith("Q") or k == "Qt"})

if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "tasks.json")
SETTINGS_FILE = os.path.join(BASE, "settings.json")


def resource_path(name):
    return os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), name)


# ---------- الثيمات ----------
THEMES = {
    "paper": {"name": "دفتر ورقي", "BG": "#f3ead9", "CARD": "#fdf8ee", "HEADER": "#f3ead9", "HEAD": "#5a4030",
              "PRIMARY": "#b4572b", "GREEN": "#6b8e3d", "RED": "#b03a2e", "GRAY": "#8d7a68", "GRAY_L": "#eadfc8",
              "BORDER": "#dccbb0", "TEXT": "#3b2c20", "HFG": "#5a4030", "DASH": True, "BW": 2, "RAD": 4},
    "glass": {"name": "زجاجي ملوّن", "BG": "#5f55ee", "CARD": "#7a71f4", "HEADER": "#5f55ee", "HEAD": "#ffffff",
              "PRIMARY": "#ffffff", "BTN_TXT": "#4b3fd6", "GREEN": "#5cffb0", "OKT": "#05402a", "RED": "#ff6b81",
              "GRAY": "#e4e1ff", "GRAY_L": "#8d85f7", "BORDER": "#9a92f9", "TEXT": "#ffffff",
              "BGC": "qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #6a5cff,stop:1 #1ec8e6)",
              "HDC": "rgba(255,255,255,0.12)", "CARDC": "rgba(255,255,255,0.20)", "BDC": "rgba(255,255,255,0.40)",
              "INC": "rgba(255,255,255,0.16)", "GLC": "rgba(255,255,255,0.22)"},
    "light": {"name": "فاتح", "BG": "#eef1f8", "CARD": "#ffffff", "HEADER": "#1e2a5a", "HEAD": "#1e2a5a",
              "PRIMARY": "#4263eb", "GREEN": "#2f9e44", "RED": "#e03131", "GRAY": "#868e96", "GRAY_L": "#f1f3f5",
              "BORDER": "#dfe3ee", "TEXT": "#212529", "HFG": "#ffffff"},
    "dark": {"name": "داكن", "BG": "#14161c", "CARD": "#1f232d", "HEADER": "#191c25", "HEAD": "#e9ecef",
             "PRIMARY": "#5c7cfa", "GREEN": "#37b24d", "RED": "#fa5252", "GRAY": "#9a9fa8", "GRAY_L": "#2b303b",
             "BORDER": "#313744", "TEXT": "#e9ecef", "HFG": "#ffffff"},
    "warm": {"name": "دافئ", "BG": "#f6efe6", "CARD": "#fffaf3", "HEADER": "#5b4636", "HEAD": "#5b4636",
             "PRIMARY": "#c2691f", "GREEN": "#5f8f3e", "RED": "#c0392b", "GRAY": "#8a7967", "GRAY_L": "#efe4d4",
             "BORDER": "#e2d3bf", "TEXT": "#3e2f23", "HFG": "#ffffff"},
    "nature": {"name": "طبيعي", "BG": "#eef4ee", "CARD": "#fbfdfb", "HEADER": "#2f5d3a", "HEAD": "#2f5d3a",
               "PRIMARY": "#2b8a7b", "GREEN": "#2f9e44", "RED": "#c92a2a", "GRAY": "#7b8a7d", "GRAY_L": "#e3ece4",
               "BORDER": "#d0ddd1", "TEXT": "#1f2d22", "HFG": "#ffffff"},
}
SETTINGS = {"theme": "paper", "scale": 100}
ACCENTS = ["#4263eb", "#f76707", "#12b886", "#e64980", "#7048e8", "#1098ad"]
ICONS = ["book", "calc", "flask", "globe", "pencil", "atom", "openbook", "bulb"]
DAYS_AR = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
MONTHS_AR = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر",
             "أكتوبر", "نوفمبر", "ديسمبر"]
QUOTES = ["خطوة صغيرة كل يوم تصنع فرقاً كبيراً", "ركّز على اليوم، والباقي يجي لحاله",
          "الإنجاز يبدأ بأول سطر تكتبه", "ما عليك تكمل كل شي، بس ابدأ",
          "عقلك أقوى مما تتخيل", "كل يوم تخلصه يقربك من هدفك"]


def T():
    return THEMES[SETTINGS["theme"]]


def P(n):
    return round(n * SETTINGS["scale"] / 100)


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            SETTINGS.update(json.load(f))
    except Exception:
        pass
    if SETTINGS["theme"] not in THEMES:
        SETTINGS["theme"] = "paper"


def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(SETTINGS, f, ensure_ascii=False)


def load_tasks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def greeting():
    h = time.localtime().tm_hour
    return (("moon", "سهران؟ ركّز شوي") if h < 5 else ("sun", "صباح الخير") if h < 12
            else ("cloudsun", "طاب يومك") if h < 17 else ("sunset", "مساء الخير") if h < 21
            else ("moon", "مساء النور"))


def arabic_date():
    t = time.localtime()
    return f"{DAYS_AR[t.tm_wday]} {t.tm_mday} {MONTHS_AR[t.tm_mon - 1]}"


def mix(a, b, t):
    ca, cb = QColor(a), QColor(b)
    return QColor(round(ca.red() + (cb.red() - ca.red()) * t), round(ca.green() + (cb.green() - ca.green()) * t),
                  round(ca.blue() + (cb.blue() - ca.blue()) * t)).name()


def tint(c, a=0.18):
    q = QColor(c)
    return f"rgba({q.red()},{q.green()},{q.blue()},{a})"


# ---------- رسومات الأيقونات (بدل الإيموجي) ----------
def _pts(pts, close=False):
    path = QPainterPath(QPointF(*pts[0]))
    for q in pts[1:]:
        path.lineTo(QPointF(*q))
    if close:
        path.closeSubpath()
    return path


def _draw(name, p, c):
    L = lambda *pts: p.drawPath(_pts(pts))
    Z = lambda *pts: p.drawPath(_pts(pts, True))
    O = lambda x, y, rx, ry=None: p.drawEllipse(QPointF(x, y), rx, ry or rx)
    R = lambda x, y, w, h, r=2: p.drawRoundedRect(QRectF(x, y, w, h), r, r)
    dots = lambda *pts: [p.drawPoint(QPointF(*q)) for q in pts]
    if name == "plus":
        L((12, 5), (12, 19)); L((5, 12), (19, 12))
    elif name == "close":
        L((6, 6), (18, 18)); L((18, 6), (6, 18))
    elif name == "back":
        L((5, 12), (19, 12)); L((13, 6), (19, 12), (13, 18))
    elif name == "check":
        L((5, 13), (10, 18), (19, 7))
    elif name == "checkcircle":
        O(12, 12, 9); L((8, 12.5), (11, 15.5), (16, 9))
    elif name == "gear":
        O(12, 12, 6.5); O(12, 12, 2.5)
        for k in range(8):
            a = k * math.pi / 4
            L((12 + 6.5 * math.cos(a), 12 + 6.5 * math.sin(a)), (12 + 9.5 * math.cos(a), 12 + 9.5 * math.sin(a)))
    elif name == "timer":
        O(12, 13.5, 7.5); L((12, 13.5), (15, 10.5)); L((9.5, 3), (14.5, 3)); L((12, 3), (12, 6))
    elif name == "book":
        R(5, 3, 14, 18); L((9, 3), (9, 21)); L((12.5, 8), (16, 8))
    elif name == "openbook":
        path = QPainterPath(QPointF(12, 6))
        path.cubicTo(10, 4, 6, 4, 3, 5); path.lineTo(3, 19); path.cubicTo(6, 18, 10, 18, 12, 20)
        path.cubicTo(14, 18, 18, 18, 21, 19); path.lineTo(21, 5); path.cubicTo(18, 4, 14, 4, 12, 6)
        p.drawPath(path); L((12, 6), (12, 20))
    elif name == "calc":
        R(5, 3, 14, 18); R(8, 6, 8, 3, 1)
        p.setPen(QPen(c, 2.8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        dots((9, 13), (12, 13), (15, 13), (9, 17), (12, 17), (15, 17))
    elif name == "flask":
        L((9, 3), (15, 3)); L((10, 3), (10, 9.5), (5, 19), (6, 21), (18, 21), (19, 19), (14, 9.5), (14, 3))
        L((7.5, 15), (16.5, 15))
    elif name == "globe":
        O(12, 12, 9); O(12, 12, 4, 9); L((3, 12), (21, 12))
    elif name == "pencil":
        Z((17, 3), (21, 7), (8, 20), (3, 21), (4, 16)); L((14, 6), (18, 10))
    elif name == "atom":
        for ang in (0, 60, 120):
            p.save(); p.translate(12, 12); p.rotate(ang); p.drawEllipse(QPointF(0, 0), 10, 4); p.restore()
        p.setBrush(c); O(12, 12, 1.6)
    elif name == "bulb":
        O(12, 9.5, 6); L((9, 15), (9, 17), (15, 17), (15, 15)); L((10, 20), (14, 20))
    elif name == "list":
        R(5, 4, 14, 17); R(9, 2, 6, 4, 1); L((8, 11), (16, 11)); L((8, 15), (14, 15))
    elif name == "flame":
        path = QPainterPath(QPointF(12, 2))
        path.cubicTo(9, 6, 5, 9, 5, 14); path.cubicTo(5, 18, 8, 21, 12, 21); path.cubicTo(16, 21, 19, 18, 19, 14)
        path.cubicTo(19, 11, 17.5, 9, 16.5, 7); path.cubicTo(15.5, 9, 14.5, 10, 13.5, 10)
        path.cubicTo(14, 7, 13.5, 4.5, 12, 2)
        p.setBrush(c); p.drawPath(path)
    elif name == "sun":
        O(12, 12, 4)
        for k in range(8):
            a = k * math.pi / 4
            L((12 + 6.5 * math.cos(a), 12 + 6.5 * math.sin(a)), (12 + 9 * math.cos(a), 12 + 9 * math.sin(a)))
    elif name == "moon":
        big, cut = QPainterPath(), QPainterPath()
        big.addEllipse(QPointF(12, 12), 9, 9); cut.addEllipse(QPointF(17, 8), 7.5, 7.5)
        p.setBrush(c); p.drawPath(big.subtracted(cut))
    elif name == "cloudsun":
        O(8, 8, 3)
        for k in range(5):
            a = math.pi + k * math.pi / 4
            L((8 + 5 * math.cos(a), 8 + 5 * math.sin(a)), (8 + 7 * math.cos(a), 8 + 7 * math.sin(a)))
        cl = QPainterPath()
        for x, y, r in ((9, 16.5, 3.5), (14, 14.5, 5), (18.5, 17, 3)):
            q = QPainterPath(); q.addEllipse(QPointF(x, y), r, r); cl = cl.united(q)
        q = QPainterPath(); q.addRect(QRectF(9, 16.5, 9.5, 4)); p.drawPath(cl.united(q))
    elif name == "sunset":
        p.drawArc(QRectF(7, 9, 10, 10), 0, 180 * 16); L((3, 19), (21, 19)); L((12, 3), (12, 6))
        L((4.5, 10.5), (6.5, 12.5)); L((19.5, 10.5), (17.5, 12.5))
    elif name == "rocket":
        path = QPainterPath(QPointF(12, 2))
        path.cubicTo(16, 5, 17, 10, 15, 15); path.lineTo(9, 15); path.cubicTo(7, 10, 8, 5, 12, 2)
        p.drawPath(path); O(12, 9, 1.5)
        L((9, 12.5), (6, 16), (6, 19), (9, 17)); L((15, 12.5), (18, 16), (18, 19), (15, 17)); L((12, 17.5), (12, 21))
    elif name == "flag":
        L((5, 3), (5, 21)); L((5, 4), (18, 4), (15, 8.5), (18, 13), (5, 13))
    elif name == "star":
        pts = [(12 + (10 if i % 2 == 0 else 4.3) * math.cos(-math.pi / 2 + i * math.pi / 5),
                12.5 + (10 if i % 2 == 0 else 4.3) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)]
        p.setBrush(c); Z(*pts)


_PIX = {}


def pix(name, color, size):
    k = (name, color, size)
    if k not in _PIX:
        pm = QPixmap(size * 2, size * 2)
        pm.setDevicePixelRatio(2)
        pm.fill(Qt.GlobalColor.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.scale(size / 24, size / 24)
        c = QColor(color)
        p.setPen(QPen(c, 1.9, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        p.setBrush(Qt.BrushStyle.NoBrush)
        _draw(name, p, c)
        p.end()
        _PIX[k] = pm
    return _PIX[k]


def ilabel(name, color, size):
    l = QLabel()
    l.setPixmap(pix(name, color, size))
    l.setFixedSize(size, size)
    l.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return l


def icon_text(name, text, color, size, obj="mut", center=False):
    w = QWidget()
    h = QHBoxLayout(w)
    h.setContentsMargins(0, 0, 0, 0)
    h.setSpacing(6)
    if center:
        h.setAlignment(Qt.AlignmentFlag.AlignCenter)
    w.i, w.t = ilabel(name, color, size), lbl(text, obj)
    h.addWidget(w.i)
    h.addWidget(w.t)
    return w


def set_icon_text(w, name, text, color):
    w.i.setPixmap(pix(name, color, w.i.width()))
    w.t.setText(text)


# ---------- التنسيق (QSS) ----------
def make_qss(t, sc):
    p = lambda n: round(n * sc / 100)
    g = t.get
    card, bd, inp = g("CARDC", t["CARD"]), g("BDC", t["BORDER"]), g("INC", t["CARD"])
    ghost, rad, bw = g("GLC", t["GRAY_L"]), g("RAD", 12), g("BW", 1)

    def kind(name, bg, fg, base):
        return (f'QPushButton[kind="{name}"]{{background:{bg};color:{fg};}}'
                f'QPushButton[kind="{name}"]:hover{{background:{mix(base, "#ffffff", .2)};}}'
                f'QPushButton[kind="{name}"]:pressed{{background:{mix(base, "#000000", .2)};}}')
    dash = f'border-bottom:2px dashed {t["BORDER"]};' if g("DASH") else ""
    return f"""
* {{ font-family: Tahoma, 'Segoe UI', sans-serif; font-size: {p(14)}px; color: {t['TEXT']}; }}
QMainWindow, #root {{ background: {g('BGC', t['BG'])}; }}
QDialog, QMessageBox {{ background: {t['BG']}; }}
QLabel {{ background: transparent; }}
QScrollArea, #inner, QScrollArea > QWidget > QWidget {{ background: transparent; border: none; }}
QFrame#header {{ background: {g('HDC', t['HEADER'])}; {dash} }}
QLabel#htitle {{ color: {g('HFG', 'white')}; font-size: {p(19)}px; font-weight: bold; }}
QLabel#h {{ color: {t['HEAD']}; font-weight: bold; }}
QLabel#mut {{ color: {t['GRAY']}; font-size: {p(12)}px; }}
QFrame#card {{ background: {card}; border: {bw}px solid {bd}; border-radius: {rad}px; }}
QFrame#card:hover {{ border-color: {t['PRIMARY']}; }}
QLineEdit, QSpinBox {{ background: {inp}; border: 1px solid {bd}; border-radius: 8px; padding: 7px 10px;
    selection-background-color: {t['PRIMARY']}; selection-color: {g('BTN_TXT', 'white')}; }}
QLineEdit:focus, QSpinBox:focus {{ border: 1px solid {t['PRIMARY']}; }}
QPushButton {{ border: none; border-radius: {max(rad - 2, 3)}px; padding: 8px 18px; font-weight: bold; }}
{kind('primary', t['PRIMARY'], g('BTN_TXT', 'white'), t['PRIMARY'])}
{kind('green', t['GREEN'], g('OKT', 'white'), t['GREEN'])}
{kind('red', t['RED'], 'white', t['RED'])}
{kind('ghost', ghost, t['TEXT'], t['GRAY_L'])}
QScrollBar:vertical {{ background: transparent; width: 8px; }}
QScrollBar::handle:vertical {{ background: {t['GRAY']}; border-radius: 4px; min-height: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
QSlider::groove:horizontal {{ height: 6px; background: {t['GRAY_L']}; border-radius: 3px; }}
QSlider::handle:horizontal {{ background: {t['PRIMARY']}; width: 20px; margin: -7px 0; border-radius: 10px; }}
"""


# ---------- عناصر مساعدة ----------
def kind_fg(kind):
    t = T()
    return {"primary": t.get("BTN_TXT", "white"), "green": t.get("OKT", "white"), "red": "white"}.get(kind, t["TEXT"])


def _seticon(b):
    if getattr(b, "_ico", None):
        b.setIcon(QIcon(pix(b._ico, kind_fg(b.property("kind")), P(18))))
        b.setIconSize(QSize(P(18), P(18)))
    else:
        b.setIcon(QIcon())


def btn(text, kind="primary", cb=None, icon=None):
    b = QPushButton(text)
    b.setProperty("kind", kind)
    b._ico = icon
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    if cb:
        b.clicked.connect(lambda *_: cb())
    _seticon(b)
    return b


def set_kind(b, kind, icon="keep"):
    b.setProperty("kind", kind)
    if icon != "keep":
        b._ico = icon
    b.style().unpolish(b)
    b.style().polish(b)
    _seticon(b)


def lbl(text="", name=None, align=None):
    l = QLabel(text)
    if name:
        l.setObjectName(name)
    if align:
        l.setAlignment(align)
    return l


def header(title, right=None, left=None, icon=None):
    f = QFrame()
    f.setObjectName("header")
    h = QHBoxLayout(f)
    h.setContentsMargins(14, 12, 14, 12)
    if right:
        h.addWidget(right)
    h.addStretch()
    if icon:
        h.addWidget(ilabel(icon, T().get("HFG", "white"), P(26)))
    h.addWidget(lbl(title, "htitle"))
    h.addStretch()
    if left:
        h.addWidget(left)
    return f


def scroll():
    a = QScrollArea()
    a.setWidgetResizable(True)
    a.setFrameShape(QFrame.Shape.NoFrame)
    inner = QWidget()
    inner.setObjectName("inner")
    lay = QVBoxLayout(inner)
    lay.setAlignment(Qt.AlignmentFlag.AlignTop)
    lay.setSpacing(10)
    lay.setContentsMargins(0, 0, 6, 0)
    a.setWidget(inner)
    return a, lay


def clear(lay):
    while lay.count():
        w = lay.takeAt(0).widget()
        if w:
            w.setParent(None)
            w.deleteLater()


def anim(parent, a, b, ms, cb, ease=QEasingCurve.Type.OutCubic):
    v = QVariantAnimation(parent)
    v.setStartValue(float(a))
    v.setEndValue(float(b))
    v.setDuration(ms)
    v.setEasingCurve(ease)
    v.valueChanged.connect(lambda x: cb(float(x)))
    v.start()
    return v


def fade(w, delay=0, ms=280):
    eff = QGraphicsOpacityEffect(w)
    eff.setOpacity(0)
    w.setGraphicsEffect(eff)
    a = QPropertyAnimation(eff, b"opacity", w)
    a.setDuration(ms)
    a.setStartValue(0.0)
    a.setEndValue(1.0)
    a.finished.connect(lambda: w.setGraphicsEffect(None))
    w._fa = a

    def go():
        try:
            a.start()
        except RuntimeError:
            pass
    QTimer.singleShot(delay, go)


class Card(QFrame):
    def __init__(self, on_click=None):
        super().__init__()
        self.setObjectName("card")
        self.on_click = on_click
        if on_click:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseReleaseEvent(self, e):
        if self.on_click and self.rect().contains(e.position().toPoint()):
            self.on_click()
        super().mouseReleaseEvent(e)


class Bar(QWidget):
    """شريط تقدم متحرك (ينمو من اليمين)"""
    def __init__(self, color):
        super().__init__()
        self.v, self.color = 0.0, color
        self.setFixedHeight(9)

    def set(self, a, b):
        def f(x):
            self.v = x
            self.update()
        self._a = anim(self, a, b, 650, f)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(T()["GRAY_L"]))
        p.drawRoundedRect(QRectF(self.rect()), 4.5, 4.5)
        if self.v > 0:
            w = self.width() * self.v
            p.setBrush(QColor(self.color))
            p.drawRoundedRect(QRectF(self.width() - w, 0, w, self.height()), 4.5, 4.5)


class Ring(QWidget):
    """حلقة التايمر"""
    def __init__(self):
        super().__init__()
        self.frac, self.text, self.urgent = 0.0, "00:00:00", False
        self.setFixedSize(P(165), P(165))

    def set(self, text, frac, urgent):
        self.text, self.frac, self.urgent = text, frac, urgent
        self.update()

    def paintEvent(self, e):
        t = T()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(12, 12, self.width() - 24, self.height() - 24)
        pen = QPen(QColor(t["GRAY_L"]), 11)
        p.setPen(pen)
        p.drawEllipse(r)
        if self.frac > 0:
            pen = QPen(QColor(t["RED"] if self.urgent else t["PRIMARY"]), 11)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen)
            p.drawArc(r, 90 * 16, int(-360 * 16 * self.frac))
        p.setPen(QColor(t["RED"] if self.urgent else t["HEAD"]))
        f = QFont("Tahoma")
        f.setPixelSize(P(22))
        f.setBold(True)
        p.setFont(f)
        p.drawText(r, Qt.AlignmentFlag.AlignCenter, self.text)


class Confetti(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.ps = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.step)
        self.hide()

    def burst(self, pos, n=30):
        self.setGeometry(self.parent().rect())
        self.raise_()
        self.show()
        t = T()
        cols = [t["PRIMARY"], t["GREEN"], "#fab005", "#f06595", "#22b8cf", "#ff922b"]
        for _ in range(n):
            self.ps.append([pos.x(), pos.y(), random.uniform(-7, 7), random.uniform(-13, -3),
                            QColor(random.choice(cols)), random.randint(6, 11), 70])
        if not self.timer.isActive():
            self.timer.start(16)

    def step(self):
        for p in self.ps:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.5
            p[6] -= 1
        self.ps = [p for p in self.ps if p[6] > 0]
        if not self.ps:
            self.timer.stop()
            self.hide()
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        for x, y, _, _, c, s, life in self.ps:
            c.setAlphaF(min(1.0, life / 25))
            p.fillRect(QRectF(x, y, s, s), c)


# ---------- الصفحة الرئيسية ----------
class Home(QWidget):
    def __init__(self, w):
        super().__init__()
        self.w, self.prog, self.prev = w, {}, {}
        L = QVBoxLayout(self)
        L.setContentsMargins(0, 0, 0, 0)
        L.setSpacing(0)
        L.addWidget(header("مهامي الدراسية", right=btn("إنشاء مهمة", "primary", w.open_create, "plus"),
                           left=btn("", "ghost", w.open_settings, "gear"), icon="openbook"))
        body = QVBoxLayout()
        body.setContentsMargins(18, 14, 18, 14)
        body.setSpacing(8)
        self.hello, self.sub = lbl("", "h"), lbl("", "mut")
        self.hello.setStyleSheet(f"font-size:{P(18)}px;")
        self.hico = ilabel("sun", T()["HEAD"], P(26))
        hr = QHBoxLayout()
        hr.addWidget(self.hico)
        hr.addWidget(self.hello, 1)
        body.addLayout(hr)
        body.addWidget(self.sub)
        self.stats = QHBoxLayout()
        body.addLayout(self.stats)
        self.area, self.list = scroll()
        body.addWidget(self.area, 1)
        L.addLayout(body, 1)

    def refresh(self):
        tasks = self.w.tasks
        gi, gt = greeting()
        self.hello.setText(gt)
        self.hico.setPixmap(pix(gi, T()["HEAD"], P(26)))
        self.sub.setText(f"{arabic_date()}  •  {random.choice(QUOTES)}")
        done = sum(d["done"] for t in tasks for d in t["days"])
        total = sum(len(t["days"]) for t in tasks)
        pct = round(done * 100 / total) if total else 0
        clear(self.stats)
        for key, ico, val, suf in (("المهام", "list", len(tasks), ""), ("أيام منجزة", "checkcircle", done, ""),
                                   ("الإنجاز", "flame", pct, "%")):
            c = Card()
            v = QVBoxLayout(c)
            v.setSpacing(0)
            num = lbl("", "h", Qt.AlignmentFlag.AlignCenter)
            num.setStyleSheet(f"font-size:{P(22)}px;")
            v.addWidget(num)
            v.addWidget(icon_text(ico, key, T()["GRAY"], P(16), "mut", True))
            self.stats.addWidget(c)
            a = self.prev.get(key, 0)
            num._a = anim(num, a, val, 600, lambda x, n=num, s=suf: n.setText(f"{round(x)}{s}"))
            self.prev[key] = val
        clear(self.list)
        if not tasks:
            self.empty()
            return
        for idx, t in enumerate(tasks):
            c = self.task_card(idx, t)
            self.list.addWidget(c)
            fade(c, idx * 90)

    def empty(self):
        box = QWidget()
        v = QVBoxLayout(box)
        v.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        ico = ilabel("openbook", T()["GRAY"], P(84))
        v.addWidget(ico, 0, Qt.AlignmentFlag.AlignHCenter)
        v.addWidget(lbl("لا يوجد", "mut", Qt.AlignmentFlag.AlignCenter))
        v.addWidget(lbl("اضغط «إنشاء مهمة» وابدأ رحلتك", "mut", Qt.AlignmentFlag.AlignCenter))
        v.itemAt(1).widget().setStyleSheet(f"font-size:{P(22)}px;")
        self.list.addWidget(box)

        def f(x):
            v.setContentsMargins(0, 40 - round(abs(math.sin(x)) * 28), 0, round(abs(math.sin(x)) * 28))
        box._a = QVariantAnimation(box)
        box._a.setStartValue(0.0)
        box._a.setEndValue(6.2832)
        box._a.setDuration(1500)
        box._a.setLoopCount(-1)
        box._a.valueChanged.connect(lambda x: f(float(x)))
        box._a.start()

    def task_card(self, idx, t):
        done, total = sum(d["done"] for d in t["days"]), len(t["days"])
        color = t.get("color") or ACCENTS[idx % len(ACCENTS)]
        icon = t.get("icon")
        icon = icon if icon in ICONS else ICONS[idx % len(ICONS)]
        c = Card(lambda t=t: self.w.open_task(t))
        h = QHBoxLayout(c)
        h.setContentsMargins(12, 12, 16, 12)
        h.setSpacing(12)
        stripe = QFrame()
        stripe.setFixedWidth(5)
        stripe.setStyleSheet(f"background:{T()['GREEN'] if done == total else color};border-radius:2px;")
        h.addWidget(stripe)
        col = QVBoxLayout()
        col.setSpacing(6)
        top = QHBoxLayout()
        ic = ilabel(icon, color, P(28))
        ic.setFixedSize(P(46), P(46))
        ic.setStyleSheet(f"background:{tint(color, .22)};border-radius:12px;")
        top.addWidget(ic)
        name = lbl(t["name"], "h")
        name.setStyleSheet(f"font-size:{P(19)}px;")
        top.addWidget(name, 1)
        col.addLayout(top)
        if done == total:
            st = icon_text("check", "مكتملة", T()["GREEN"], P(16), "mut")
            st.t.setStyleSheet(f"color:{T()['GREEN']};")
        else:
            st = lbl(f"أُنجز {done} من {total} يوم", "mut")
        col.addWidget(st)
        bar = Bar(T()["GREEN"] if done == total else color)
        bar.set(self.prog.get(id(t), 0), done / total if total else 0)
        self.prog[id(t)] = done / total if total else 0
        col.addWidget(bar)
        row = QHBoxLayout()
        row.addWidget(btn("العمل على المهمة", "primary", lambda t=t: self.w.open_task(t)))
        row.addStretch()
        row.addWidget(btn("حذف", "ghost", lambda t=t: self.delete(t)))
        col.addLayout(row)
        h.addLayout(col, 1)
        return c

    def delete(self, t):
        if QMessageBox.question(self, "حذف", f"تحذف مهمة «{t['name']}»؟") == QMessageBox.StandardButton.Yes:
            self.w.tasks.remove(t)
            save_tasks(self.w.tasks)
            self.refresh()


# ---------- صفحة إنشاء مهمة ----------
class Create(QWidget):
    def __init__(self, w):
        super().__init__()
        self.w, self.edits = w, []
        L = QVBoxLayout(self)
        L.setContentsMargins(0, 0, 0, 0)
        L.setSpacing(0)
        L.addWidget(header("مهمة جديدة", left=btn("إغلاق", "red", w.close_create, "close")))
        body = QVBoxLayout()
        body.setContentsMargins(18, 14, 18, 16)
        body.setSpacing(6)
        body.addWidget(lbl("1- اسم المهمة", "h"))
        self.name = QLineEdit()
        self.name.setPlaceholderText("مثال: مراجعة الرياضيات")
        body.addWidget(self.name)
        body.addWidget(lbl("2- عدد الأيام", "h"))
        self.days = QSpinBox()
        self.days.setRange(1, 60)
        self.days.setValue(3)
        self.days.valueChanged.connect(lambda *_: self.build_days())
        body.addWidget(self.days)
        body.addWidget(lbl("3- وش تسوي في كل يوم؟ (اختياري)", "h"))
        self.area, self.dl = scroll()
        body.addWidget(self.area, 1)
        body.addWidget(btn("إنشاء", "green", self.make))
        L.addLayout(body, 1)
        self.build_days()

    def build_days(self):
        old = [e.text() for e in self.edits]
        clear(self.dl)
        self.edits = []
        for i in range(self.days.value()):
            r = QHBoxLayout()
            e = QLineEdit()
            e.setPlaceholderText("فاضي")
            if i < len(old):
                e.setText(old[i])
            self.edits.append(e)
            holder = QWidget()
            holder.setLayout(r)
            r.setContentsMargins(0, 0, 0, 0)
            r.addWidget(lbl(f"اليوم {i + 1}", "h"))
            r.addWidget(e, 1)
            self.dl.addWidget(holder)

    def reset(self):
        self.name.clear()
        self.days.setValue(3)
        for e in self.edits:
            e.clear()
        self.build_days()

    def make(self):
        name = self.name.text().strip()
        if not name:
            QMessageBox.warning(self, "تنبيه", "اكتب اسم المهمة")
            return
        n = len(self.w.tasks)
        self.w.tasks.append({"name": name, "color": ACCENTS[n % len(ACCENTS)], "icon": ICONS[n % len(ICONS)],
                             "days": [{"todo": e.text().strip(), "done": False} for e in self.edits]})
        save_tasks(self.w.tasks)
        self.w.close_create()


# ---------- صفحة المهمة ----------
class TaskPage(QWidget):
    def __init__(self, w):
        super().__init__()
        self.w, self.task, self.btns = w, None, []
        self.remaining = self.total = 0
        self.running = False
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)
        L = QVBoxLayout(self)
        L.setContentsMargins(0, 0, 0, 0)
        L.setSpacing(0)
        self.head = header("", left=btn("رجوع", "ghost", self.back, "back"))
        self.title = self.head.findChild(QLabel, "htitle")
        L.addWidget(self.head)
        body = QVBoxLayout()
        body.setContentsMargins(18, 10, 18, 14)
        body.setSpacing(10)
        self.msg = icon_text("flame", "", T()["GRAY"], P(18), "mut", True)
        body.addWidget(self.msg)
        top = QHBoxLayout()
        tc = Card()
        tv = QVBoxLayout(tc)
        tv.addWidget(icon_text("timer", "التايمر", T()["HEAD"], P(20), "h"))
        inp = QHBoxLayout()
        self.h, self.m = QLineEdit(), QLineEdit()
        for e in (self.h, self.m):
            e.setFixedWidth(P(64))
            e.setAlignment(Qt.AlignmentFlag.AlignCenter)
            e.setValidator(QIntValidator(0, 999))
            e.textChanged.connect(lambda *_: None if self.running else self.reset())
        for text, e in (("ساعة", self.h), ("دقيقة", self.m)):
            inp.addWidget(lbl(text, "mut"))
            inp.addWidget(e)
        inp.addStretch()
        tv.addLayout(inp)
        self.ring = Ring()
        tv.addWidget(self.ring, 0, Qt.AlignmentFlag.AlignCenter)
        br = QHBoxLayout()
        self.start = btn("ابدأ", "green", self.toggle_timer)
        br.addWidget(self.start)
        br.addWidget(btn("إعادة", "ghost", self.reset))
        tv.addLayout(br)
        top.addWidget(tc)
        lc = Card()
        lv = QVBoxLayout(lc)
        lv.addWidget(lbl("المتبقي", "mut", Qt.AlignmentFlag.AlignCenter))
        self.num = lbl("", "h", Qt.AlignmentFlag.AlignCenter)
        lv.addWidget(self.num)
        self.numtxt = lbl("", "mut", Qt.AlignmentFlag.AlignCenter)
        lv.addWidget(self.numtxt)
        lv.addStretch()
        top.addWidget(lc, 1)
        body.addLayout(top)
        self.area, self.rl = scroll()
        body.addWidget(self.area, 1)
        L.addLayout(body, 1)
        self.conf = Confetti(self)

    def load(self, task):
        self.task = task
        self.title.setText(task["name"])
        clear(self.rl)
        self.btns = []
        for i, d in enumerate(task["days"]):
            r = self.make_row(i, d)
            self.rl.addWidget(r)
            fade(r, min(i * 45, 600))
        self.h.blockSignals(True)
        self.m.blockSignals(True)
        self.h.clear()
        self.m.clear()
        self.h.blockSignals(False)
        self.m.blockSignals(False)
        self.reset()
        self.update_left()

    def make_row(self, i, d):
        accent = self.task.get("color") or T()["PRIMARY"]
        c = Card()
        h = QHBoxLayout(c)
        badge = lbl(f"اليوم {i + 1}", "h", Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"background:{tint(accent, .22)};border-radius:8px;padding:5px 10px;")
        h.addWidget(badge)
        e = QLineEdit(d["todo"])
        e.setPlaceholderText("اضغط واكتب المطلوب...")
        e.textChanged.connect(lambda txt, d=d: (d.__setitem__("todo", txt.strip()), save_tasks(self.w.tasks)))
        h.addWidget(e, 1)
        b = btn("", "ghost", lambda i=i: self.toggle_day(i))
        b.setFixedWidth(P(130))
        self.btns.append(b)
        self.style_btn(b, d)
        h.addWidget(b)
        return c

    def style_btn(self, b, d):
        b.setText("مكتمل" if d["done"] else "إكمال المهمة")
        set_kind(b, "green" if d["done"] else "ghost", "check" if d["done"] else None)

    def toggle_day(self, i):
        d = self.task["days"][i]
        d["done"] = not d["done"]
        save_tasks(self.w.tasks)
        self.style_btn(self.btns[i], d)
        self.update_left()
        if d["done"]:
            b = self.btns[i]
            if all(x["done"] for x in self.task["days"]):
                self.conf.burst(QPoint(self.width() // 2, self.height() // 3), 90)
            else:
                self.conf.burst(b.mapTo(self, b.rect().center()), 32)

    def update_left(self):
        days = self.task["days"]
        total, left = len(days), sum(not d["done"] for d in days)
        ic, tx = (("star", "ما شاء الله خلصت المهمة كلها") if left == 0
                  else ("rocket", "يلا نبدأ أول يوم") if left == total
                  else ("flag", "باقي يوم واحد وتخلص") if left == 1
                  else ("flame", f"ممتاز! أنجزت {total - left} من {total}"))
        set_icon_text(self.msg, ic, tx, T()["GRAY"])
        self.num.clear()
        if left == 0:
            self.num.setPixmap(pix("star", T()["GREEN"], P(54)))
        else:
            self.num.setText(str(left))
        self.numtxt.setText("خلصت المهمة!" if left == 0 else "يوم باقي")
        anim(self, 0, 1, 350, lambda x: self.num.setStyleSheet(f"font-size:{P(36) + round(14 * (1 - x))}px;"),
             QEasingCurve.Type.OutBack)

    # ----- التايمر -----
    def read_seconds(self):
        return int(self.h.text() or 0) * 3600 + int(self.m.text() or 0) * 60

    def show_time(self):
        r = self.remaining
        self.ring.set(f"{r // 3600:02d}:{(r % 3600) // 60:02d}:{r % 60:02d}",
                      r / self.total if self.total else 0, self.running and 0 < r <= 10)

    def reset(self):
        self.timer.stop()
        self.running = False
        self.remaining = self.total = self.read_seconds()
        self.start.setText("ابدأ")
        set_kind(self.start, "green")
        self.show_time()

    def toggle_timer(self):
        if self.running:
            self.timer.stop()
            self.running = False
            self.start.setText("استمرار")
            set_kind(self.start, "green")
            return
        if self.remaining <= 0:
            self.remaining = self.total = self.read_seconds()
        if self.remaining <= 0:
            QMessageBox.information(self, "التايمر", "حط الساعات أو الدقائق أول")
            return
        self.running = True
        self.start.setText("إيقاف")
        set_kind(self.start, "red")
        self.timer.start()

    def tick(self):
        self.remaining -= 1
        self.show_time()
        if self.remaining <= 0:
            self.timer.stop()
            self.running = False
            self.start.setText("ابدأ")
            set_kind(self.start, "green")
            QApplication.beep()
            QMessageBox.information(self, "انتهى الوقت", "خلص وقت التايمر")

    def back(self):
        self.timer.stop()
        self.running = False
        self.w.go(self.w.home)


# ---------- صفحة الإعدادات ----------
class Settings(QWidget):
    def __init__(self, w):
        super().__init__()
        L = QVBoxLayout(self)
        L.setContentsMargins(0, 0, 0, 0)
        L.setSpacing(0)
        L.addWidget(header("الإعدادات", left=btn("إغلاق", "red", lambda: w.go(w.home), "close"), icon="gear"))
        body = QVBoxLayout()
        body.setContentsMargins(18, 16, 18, 16)
        body.addWidget(lbl("نمط الألوان", "h"))
        grid = QGridLayout()
        for i, (key, t) in enumerate(THEMES.items()):
            sel = key == SETTINGS["theme"]
            b = QPushButton(t["name"])
            if sel:
                b.setIcon(QIcon(pix("check", t["TEXT"], P(20))))
                b.setIconSize(QSize(P(20), P(20)))
            b.setMinimumHeight(P(66))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(f"QPushButton{{background:{t.get('BGC', t['BG'])};color:{t['TEXT']};"
                            f"border:3px solid {T()['PRIMARY'] if sel else T()['BORDER']};border-radius:12px;}}")
            b.clicked.connect(lambda *_, k=key: w.set_theme(k))
            grid.addWidget(b, i // 2, i % 2)
        body.addLayout(grid)
        body.addSpacing(14)
        body.addWidget(lbl("حجم الخط والعناصر", "h"))
        c = Card()
        v = QVBoxLayout(c)
        pct = lbl(f"{SETTINGS['scale']}%", "h", Qt.AlignmentFlag.AlignCenter)
        v.addWidget(pct)
        s = QSlider(Qt.Orientation.Horizontal)
        s.setRange(80, 150)
        s.setSingleStep(5)
        s.setPageStep(5)
        s.setValue(SETTINGS["scale"])
        s.valueChanged.connect(lambda x: pct.setText(f"{x}%"))
        s.sliderReleased.connect(lambda: w.set_scale(round(s.value() / 5) * 5))
        v.addWidget(s)
        v.addWidget(lbl("اسحب الشريط لتكبير أو تصغير الخط", "mut", Qt.AlignmentFlag.AlignCenter))
        body.addWidget(c)
        body.addStretch()
        L.addLayout(body, 1)


# ---------- النافذة الرئيسية (نافذة واحدة بصفحات) ----------
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مهامي الدراسية")
        self.resize(640, 800)
        for f in ("icon.ico", "icon.png"):
            if os.path.exists(resource_path(f)):
                self.setWindowIcon(QIcon(resource_path(f)))
                break
        self.tasks = load_tasks()
        self.stack = QStackedWidget()
        self.stack.setObjectName("root")
        self.setCentralWidget(self.stack)
        self.apply()
        self.build()
        self.go(self.home)

    def apply(self):
        QApplication.instance().setStyleSheet(make_qss(T(), SETTINGS["scale"]))

    def build(self):
        while self.stack.count():
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()
        self.home, self.create, self.taskp, self.settings = Home(self), Create(self), TaskPage(self), Settings(self)
        for p in (self.home, self.create, self.taskp, self.settings):
            self.stack.addWidget(p)

    def go(self, page):
        if page is self.home:
            self.home.refresh()
        self.stack.setCurrentWidget(page)
        fade(page, 0, 220)

    def open_create(self):
        self.create.reset()
        self.go(self.create)

    def close_create(self):
        self.go(self.home)

    def open_task(self, t):
        self.taskp.load(t)
        self.go(self.taskp)

    def open_settings(self):
        self.go(self.settings)

    def set_theme(self, key):
        SETTINGS["theme"] = key
        self.changed()

    def set_scale(self, v):
        if v != SETTINGS["scale"]:
            SETTINGS["scale"] = v
            self.changed()

    def changed(self):
        save_settings()
        self.apply()
        self.build()
        self.go(self.settings)


def main():
    load_settings()
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    w = Window()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
