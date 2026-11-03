#!/usr/bin/env python3
import subprocess
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib

STEP = "5%"

CSS = b"""
window {
    background: #16161a;
    border-radius: 18px;
    border: 1px solid #2a2a33;
}
.value {
    font-size: 34px;
    font-weight: 700;
    color: #f2f2f5;
}
.caption {
    font-size: 11px;
    letter-spacing: 2px;
    color: #7c7c8a;
}
progressbar trough {
    min-height: 6px;
    border-radius: 3px;
    background: #26262e;
}
progressbar progress {
    min-height: 6px;
    border-radius: 3px;
    background: #e8c170;
}
button.step {
    font-size: 22px;
    font-weight: 600;
    min-width: 64px;
    min-height: 44px;
    border-radius: 12px;
    border: none;
    box-shadow: none;
    background: #23232b;
    color: #f2f2f5;
}
button.step:hover  { background: #2f2f3a; }
button.step:active { background: #e8c170; color: #16161a; }
"""


def get_percent() -> int:
    try:
        out = subprocess.check_output(["brightnessctl", "-m"], text=True)
        return int(out.strip().split(",")[3].rstrip("%"))
    except Exception:
        return 0


def change(direction: str) -> None:
    sign = "+" if direction == "up" else "-"
    subprocess.run(["brightnessctl", "-n1", "set", f"{STEP}{sign}"],
                   stdout=subprocess.DEVNULL)


class BrightControl(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="brightcontrol")

    def do_activate(self):
        win = Gtk.ApplicationWindow(application=self)
        win.set_title("brightcontrol")
        win.set_decorated(False)
        win.set_resizable(False)
        win.set_default_size(260, 150)

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        for m in ("top", "bottom", "start", "end"):
            getattr(box, f"set_margin_{m}")(18)

        caption = Gtk.Label(label="BRILHO", xalign=0)
        caption.add_css_class("caption")

        self.value = Gtk.Label(xalign=0)
        self.value.add_css_class("value")

        self.bar = Gtk.ProgressBar()

        buttons = Gtk.Box(spacing=10, homogeneous=True)
        dec = Gtk.Button(label="−")
        inc = Gtk.Button(label="+")
        for b in (dec, inc):
            b.add_css_class("step")
            buttons.append(b)
        dec.connect("clicked", lambda *_: self.adjust("down"))
        inc.connect("clicked", lambda *_: self.adjust("up"))

        for w in (caption, self.value, self.bar, buttons):
            box.append(w)
        win.set_child(box)

        keys = Gtk.EventControllerKey()

        def on_key(_c, keyval, *_):
            if keyval == Gdk.KEY_Escape:
                self.quit()
            elif keyval in (Gdk.KEY_plus, Gdk.KEY_equal, Gdk.KEY_Right, Gdk.KEY_Up):
                self.adjust("up")
            elif keyval in (Gdk.KEY_minus, Gdk.KEY_Left, Gdk.KEY_Down):
                self.adjust("down")
            return True

        keys.connect("key-pressed", on_key)
        win.add_controller(keys)

        scroll = Gtk.EventControllerScroll(
            flags=Gtk.EventControllerScrollFlags.VERTICAL)
        scroll.connect("scroll", lambda _c, _dx, dy:
                       self.adjust("down" if dy > 0 else "up"))
        win.add_controller(scroll)

        def arm_focus_close():
            win.connect("notify::is-active",
                        lambda w, _p: None if w.is_active() else self.quit())
            return False

        GLib.timeout_add(400, arm_focus_close)

        self.refresh()
        win.present()

    def adjust(self, direction):
        change(direction)
        self.refresh()

    def refresh(self):
        p = get_percent()
        self.value.set_text(f"{p}%")
        self.bar.set_fraction(p / 100)


if __name__ == "__main__":
    BrightControl().run()
