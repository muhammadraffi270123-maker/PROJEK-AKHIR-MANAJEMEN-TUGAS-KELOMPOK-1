"""
TaskMaster - Aplikasi Manajemen Tugas (Desktop GUI)
Tanpa fitur kategori.
Deadline pakai date picker (klik kalender).
Jalankan: python taskmaster_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import os
import calendar
from datetime import datetime, date

# =====================================================
# KONSTANTA
# =====================================================
DATA_FILE = "tasks_data.json"
PRIORITY_LABEL = {"high": "Tinggi", "medium": "Sedang", "low": "Rendah"}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_COLOR = {"high": "#ef4444", "medium": "#f59e0b", "low": "#10b981"}


# =====================================================
# STORAGE
# =====================================================
class Storage:
    @staticmethod
    def load():
        if not os.path.exists(DATA_FILE):
            return {"tasks": []}
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                data.setdefault("tasks", [])
                return data
        except Exception:
            return {"tasks": []}

    @staticmethod
    def save(data):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# =====================================================
# HELPER
# =====================================================
def uid():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")


def is_overdue(task):
    if not task.get("deadline") or task.get("done"):
        return False
    try:
        dl = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
        return dl < date.today()
    except ValueError:
        return False


def format_date(s):
    if not s:
        return ""
    try:
        d = datetime.strptime(s, "%Y-%m-%d").date()
        bulan = ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Agu","Sep","Okt","Nov","Des"]
        return f"{d.day:02d} {bulan[d.month-1]} {d.year}"
    except ValueError:
        return s


# =====================================================
# DATE PICKER (custom, tanpa install library)
# =====================================================
class DatePicker(tk.Toplevel):
    def __init__(self, parent, initial=None, on_select=None):
        super().__init__(parent)
        self.title("Pilih Tanggal")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.on_select = on_select

        today = date.today()
        if initial:
            try:
                self.current = datetime.strptime(initial, "%Y-%m-%d").date()
            except ValueError:
                self.current = today
        else:
            self.current = today

        self.year = self.current.year
        self.month = self.current.month

        self._build()
        self._center(parent)

    def _center(self, parent):
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2 - self.winfo_width() // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2 - self.winfo_height() // 2
        self.geometry(f"+{px}+{py}")

    def _build(self):
        header = tk.Frame(self)
        header.pack(fill="x", padx=8, pady=8)

        tk.Button(header, text="◀", command=self.prev_month,
                  relief="flat", width=3).pack(side="left")
        self.month_label = tk.Label(header, font=("Segoe UI", 11, "bold"))
        self.month_label.pack(side="left", expand=True)
        tk.Button(header, text="▶", command=self.next_month,
                  relief="flat", width=3).pack(side="right")

        days_frame = tk.Frame(self)
        days_frame.pack(padx=8)
        for i, d in enumerate(["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]):
            fg = "#ef4444" if i >= 5 else "#6b7280"
            tk.Label(days_frame, text=d, width=4, font=("Segoe UI", 8, "bold"),
                     fg=fg).grid(row=0, column=i, pady=(0, 4))

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(padx=8, pady=(0, 8))

        bottom = tk.Frame(self)
        bottom.pack(fill="x", padx=8, pady=(0, 8))
        tk.Button(bottom, text="Hari Ini", command=self.pick_today,
                  relief="flat", bg="#e0e7ff").pack(side="left")
        tk.Button(bottom, text="Hapus", command=self.pick_none,
                  relief="flat", bg="#fee2e2").pack(side="left", padx=4)
        tk.Button(bottom, text="Batal", command=self.destroy,
                  relief="flat").pack(side="right")

        self._draw_calendar()

    def _draw_calendar(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()

        bulan_nama = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                      "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        self.month_label.config(text=f"{bulan_nama[self.month-1]} {self.year}")

        cal = calendar.Calendar(firstweekday=0)
        weeks = cal.monthdayscalendar(self.year, self.month)
        today = date.today()

        for r, week in enumerate(weeks):
            for c, day in enumerate(week):
                if day == 0:
                    tk.Label(self.grid_frame, text="", width=4).grid(row=r, column=c)
                    continue

                d = date(self.year, self.month, day)
                is_today = (d == today)
                is_selected = (d == self.current)

                if is_selected:
                    bg, fg = "#6366f1", "white"
                elif is_today:
                    bg, fg = "#e0e7ff", "#1f2333"
                else:
                    bg, fg = "white", "#1f2333"

                btn = tk.Button(self.grid_frame, text=str(day), width=4,
                                relief="flat", bg=bg, fg=fg,
                                activebackground="#c7d2fe",
                                command=lambda dd=d: self._select(dd))
                btn.grid(row=r, column=c, padx=1, pady=1)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self._draw_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self._draw_calendar()

    def pick_today(self):
        self._select(date.today())

    def pick_none(self):
        if self.on_select:
            self.on_select("")
        self.destroy()

    def _select(self, d):
        if self.on_select:
            self.on_select(d.strftime("%Y-%m-%d"))
        self.destroy()


# =====================================================
# APLIKASI UTAMA
# =====================================================
class TaskMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📋 TaskMaster - Manajemen Tugas")
        self.root.geometry("920x700")
        self.root.minsize(700, 500)

        data = Storage.load()
        self.tasks = data["tasks"]

        self._build_ui()
        self.refresh_tasks()

    # -------------------------------------------------
    # BUILD UI
    # -------------------------------------------------
    def _build_ui(self):
        # === HEADER ===
        header = tk.Frame(self.root, bg="#6366f1", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="📋 TaskMaster", bg="#6366f1", fg="white",
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=20, pady=12)
        tk.Button(header, text="⬇️ Export", command=self.export_data,
                  bg="#4f46e5", fg="white", relief="flat", padx=10).pack(side="right", padx=5, pady=12)
        tk.Button(header, text="⬆️ Import", command=self.import_data,
                  bg="#4f46e5", fg="white", relief="flat", padx=10).pack(side="right", padx=5, pady=12)

        # === STATISTIK ===
        stats = tk.Frame(self.root, bg="#f3f4f8")
        stats.pack(fill="x", padx=16, pady=(12, 6))
        self.stat_vars = {}
        for key, label, color in [
            ("total", "Total", "#6366f1"),
            ("done", "Selesai", "#10b981"),
            ("active", "Aktif", "#f59e0b"),
            ("late", "Terlambat", "#ef4444"),
        ]:
            card = tk.Frame(stats, bg="white", relief="flat", bd=1)
            card.pack(side="left", expand=True, fill="x", padx=4, ipady=8)
            tk.Frame(card, bg=color, height=3).pack(fill="x")
            v = tk.StringVar(value="0")
            self.stat_vars[key] = v
            tk.Label(card, textvariable=v, font=("Segoe UI", 18, "bold"),
                     bg="white", fg="#1f2333").pack()
            tk.Label(card, text=label, font=("Segoe UI", 9),
                     bg="white", fg="#6b7280").pack()

        # === FORM TAMBAH ===
        form = tk.LabelFrame(self.root, text=" Tambah Tugas Baru ",
                             bg="#f3f4f8", padx=10, pady=10, font=("Segoe UI", 10, "bold"))
        form.pack(fill="x", padx=16, pady=8)

        row1 = tk.Frame(form, bg="#f3f4f8")
        row1.pack(fill="x", pady=2)
        tk.Label(row1, text="Judul:", bg="#f3f4f8").pack(side="left")
        self.title_entry = tk.Entry(row1, font=("Segoe UI", 10))
        self.title_entry.pack(side="left", fill="x", expand=True, padx=6)
        self.title_entry.bind("<Return>", lambda e: self.add_task())

        row2 = tk.Frame(form, bg="#f3f4f8")
        row2.pack(fill="x", pady=4)

        tk.Label(row2, text="Prioritas:", bg="#f3f4f8").pack(side="left")
        self.priority_var = tk.StringVar(value="Sedang")
        ttk.Combobox(row2, textvariable=self.priority_var, state="readonly", width=10,
                     values=["Tinggi", "Sedang", "Rendah"]).pack(side="left", padx=(4, 16))
        self.prio_map = {"Tinggi": "high", "Sedang": "medium", "Rendah": "low"}

        # Deadline dengan date picker
        tk.Label(row2, text="Deadline:", bg="#f3f4f8").pack(side="left")
        self.deadline_var = tk.StringVar(value="")
        tk.Entry(row2, textvariable=self.deadline_var, width=14,
                 state="readonly").pack(side="left", padx=(4, 2))
        tk.Button(row2, text="📅", command=self.open_date_picker,
                  relief="flat", bg="#e0e7ff", width=3).pack(side="left")
        tk.Button(row2, text="✕", command=lambda: self.deadline_var.set(""),
                  relief="flat", bg="#fee2e2", width=2).pack(side="left", padx=(2, 0))

        row3 = tk.Frame(form, bg="#f3f4f8")
        row3.pack(fill="x", pady=2)
        tk.Label(row3, text="Deskripsi:", bg="#f3f4f8").pack(side="left", anchor="n")
        self.desc_text = tk.Text(row3, height=2, font=("Segoe UI", 10))
        self.desc_text.pack(side="left", fill="x", expand=True, padx=6)

        row4 = tk.Frame(form, bg="#f3f4f8")
        row4.pack(fill="x", pady=(6, 0))
        tk.Label(row4, text="Sub-tugas:", bg="#f3f4f8").pack(side="left")
        self.subtask_entry = tk.Entry(row4)
        self.subtask_entry.pack(side="left", fill="x", expand=True, padx=6)
        self.subtask_entry.bind("<Return>", lambda e: self.add_pending_subtask())
        tk.Button(row4, text="+", command=self.add_pending_subtask,
                  bg="#6366f1", fg="white", relief="flat", width=3).pack(side="left")

        self.pending_subtasks = []
        self.subtask_listbox = tk.Listbox(form, height=2)
        self.subtask_listbox.pack(fill="x", pady=(4, 4))
        self.subtask_listbox.bind("<Double-Button-1>", lambda e: self.remove_pending_subtask())

        tk.Button(form, text="Tambah Tugas", command=self.add_task,
                  bg="#6366f1", fg="white", relief="flat",
                  font=("Segoe UI", 10, "bold"), pady=6).pack(fill="x", pady=(4, 0))

        # === KONTROL FILTER ===
        controls = tk.Frame(self.root, bg="#f3f4f8")
        controls.pack(fill="x", padx=16, pady=8)

        tk.Label(controls, text="🔍", bg="#f3f4f8").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self.refresh_tasks())
        tk.Entry(controls, textvariable=self.search_var, width=22).pack(side="left", padx=4)

        tk.Label(controls, text="Status:", bg="#f3f4f8").pack(side="left", padx=(12, 2))
        self.filter_status_var = tk.StringVar(value="Semua")
        ttk.Combobox(controls, textvariable=self.filter_status_var, state="readonly", width=12,
                     values=["Semua", "Aktif", "Selesai", "Terlambat"]).pack(side="left")
        self.filter_status_var.trace("w", lambda *a: self.refresh_tasks())

        tk.Label(controls, text="Prioritas:", bg="#f3f4f8").pack(side="left", padx=(12, 2))
        self.filter_prio_var = tk.StringVar(value="Semua")
        ttk.Combobox(controls, textvariable=self.filter_prio_var, state="readonly", width=10,
                     values=["Semua", "Tinggi", "Sedang", "Rendah"]).pack(side="left")
        self.filter_prio_var.trace("w", lambda *a: self.refresh_tasks())

        tk.Label(controls, text="Urut:", bg="#f3f4f8").pack(side="left", padx=(12, 2))
        self.sort_var = tk.StringVar(value="Terbaru")
        ttk.Combobox(controls, textvariable=self.sort_var, state="readonly", width=12,
                     values=["Terbaru", "Deadline", "Prioritas", "Judul A-Z"]).pack(side="left")
        self.sort_var.trace("w", lambda *a: self.refresh_tasks())

        # === DAFTAR TUGAS ===
        container = tk.Frame(self.root, bg="#f3f4f8")
        container.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        canvas = tk.Canvas(container, bg="#f3f4f8", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.tasks_frame = tk.Frame(canvas, bg="#f3f4f8")

        self.tasks_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw", tags="inner")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig("inner", width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        self.canvas = canvas

    # -------------------------------------------------
    # DATE PICKER HANDLER
    # -------------------------------------------------
    def open_date_picker(self):
        current = self.deadline_var.get()
        DatePicker(self.root, initial=current,
                   on_select=lambda val: self.deadline_var.set(val))

    # -------------------------------------------------
    # SUBTASK PREVIEW
    # -------------------------------------------------
    def add_pending_subtask(self):
        text = self.subtask_entry.get().strip()
        if not text:
            return
        self.pending_subtasks.append(text)
        self.subtask_entry.delete(0, tk.END)
        self.refresh_pending_subtasks()

    def remove_pending_subtask(self):
        sel = self.subtask_listbox.curselection()
        if not sel:
            return
        self.pending_subtasks.pop(sel[0])
        self.refresh_pending_subtasks()

    def refresh_pending_subtasks(self):
        self.subtask_listbox.delete(0, tk.END)
        for st in self.pending_subtasks:
            self.subtask_listbox.insert(tk.END, "• " + st)

    # -------------------------------------------------
    # CRUD TUGAS
    # -------------------------------------------------
    def add_task(self):
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("Peringatan", "Judul tidak boleh kosong!")
            return

        self.tasks.append({
            "id": uid(),
            "title": title,
            "description": self.desc_text.get("1.0", tk.END).strip(),
            "priority": self.prio_map[self.priority_var.get()],
            "deadline": self.deadline_var.get().strip(),
            "done": False,
            "created_at": datetime.now().isoformat(),
            "subtasks": [
                {"id": uid() + str(i), "text": s, "done": False}
                for i, s in enumerate(self.pending_subtasks)
            ],
        })

        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.deadline_var.set("")
        self.pending_subtasks.clear()
        self.refresh_pending_subtasks()

        self.save_and_refresh()

    def toggle_done(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["done"] = not t["done"]
                break
        self.save_and_refresh()

    def delete_task(self, task_id):
        if not messagebox.askyesno("Konfirmasi", "Hapus tugas ini?"):
            return
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_and_refresh()

    def edit_task(self, task_id):
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
        new = simpledialog.askstring("Edit Judul", "Judul baru:", initialvalue=task["title"])
        if new is None:
            return
        if not new.strip():
            messagebox.showwarning("Peringatan", "Judul tidak boleh kosong")
            return
        task["title"] = new.strip()
        self.save_and_refresh()

    def toggle_subtask(self, task_id, sub_id):
        for t in self.tasks:
            if t["id"] == task_id:
                for s in t["subtasks"]:
                    if s["id"] == sub_id:
                        s["done"] = not s["done"]
                        break
                break
        self.save_and_refresh()

    def add_subtask_to_task(self, task_id):
        text = simpledialog.askstring("Sub-tugas Baru", "Teks sub-tugas:")
        if not text or not text.strip():
            return
        for t in self.tasks:
            if t["id"] == task_id:
                t["subtasks"].append({"id": uid(), "text": text.strip(), "done": False})
                break
        self.save_and_refresh()

    # -------------------------------------------------
    # FILTER + SORT + RENDER
    # -------------------------------------------------
    def get_filtered_sorted(self):
        q = self.search_var.get().strip().lower()
        f_stat = self.filter_status_var.get()
        f_prio = self.filter_prio_var.get()

        result = []
        for t in self.tasks:
            if q and q not in t["title"].lower() and q not in t.get("description", "").lower():
                continue
            if f_stat == "Aktif" and t["done"]:
                continue
            if f_stat == "Selesai" and not t["done"]:
                continue
            if f_stat == "Terlambat" and not is_overdue(t):
                continue
            if f_prio != "Semua" and t["priority"] != self.prio_map[f_prio]:
                continue
            result.append(t)

        sort = self.sort_var.get()
        if sort == "Deadline":
            result.sort(key=lambda t: (t.get("deadline") or "9999-99-99"))
        elif sort == "Prioritas":
            result.sort(key=lambda t: PRIORITY_ORDER[t["priority"]])
        elif sort == "Judul A-Z":
            result.sort(key=lambda t: t["title"].lower())
        else:
            result.sort(key=lambda t: t["created_at"], reverse=True)
        return result

    def refresh_tasks(self):
        for w in self.tasks_frame.winfo_children():
            w.destroy()

        filtered = self.get_filtered_sorted()

        if not filtered:
            tk.Label(self.tasks_frame, text="Belum ada tugas yang cocok. Yuk tambahkan! 🚀",
                     bg="#f3f4f8", fg="#6b7280",
                     font=("Segoe UI", 10, "italic")).pack(pady=40)
        else:
            for task in filtered:
                self._build_task_card(task)

        self.update_stats()

    def _build_task_card(self, task):
        is_late = is_overdue(task)
        border_color = PRIORITY_COLOR[task["priority"]]

        card = tk.Frame(self.tasks_frame, bg="white", relief="flat", bd=1)
        card.pack(fill="x", pady=6, padx=2)

        tk.Frame(card, bg=border_color, width=6).pack(side="left", fill="y")

        inner = tk.Frame(card, bg="white", padx=10, pady=8)
        inner.pack(side="left", fill="both", expand=True)

        row = tk.Frame(inner, bg="white")
        row.pack(fill="x")

        done_var = tk.BooleanVar(value=task["done"])
        tk.Checkbutton(row, variable=done_var, bg="white", activebackground="white",
                       command=lambda: self.toggle_done(task["id"])).pack(side="left")

        title_text = ("⚠️ " if is_late else "") + task["title"]
        title_lbl = tk.Label(row, text=title_text, bg="white", anchor="w",
                             font=("Segoe UI", 11, "bold"),
                             fg="#9ca3af" if task["done"] else "#1f2333")
        title_lbl.pack(side="left", fill="x", expand=True, padx=4)
        if task["done"]:
            title_lbl.config(font=("Segoe UI", 11, "bold overstrike"))

        tk.Button(row, text="✏️", command=lambda: self.edit_task(task["id"]),
                  bg="white", relief="flat").pack(side="right")
        tk.Button(row, text="🗑️", command=lambda: self.delete_task(task["id"]),
                  bg="white", relief="flat").pack(side="right")

        meta = tk.Frame(inner, bg="white")
        meta.pack(fill="x", pady=(4, 0))
        tk.Label(meta, text=f"🎯 {PRIORITY_LABEL[task['priority']]}",
                 bg="white", fg=border_color, font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))
        if task.get("deadline"):
            color = "#ef4444" if is_late else "#6b7280"
            prefix = "⚠️ Terlambat: " if is_late else "📅 "
            tk.Label(meta, text=prefix + format_date(task["deadline"]),
                     bg="white", fg=color, font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))
        if task["done"]:
            tk.Label(meta, text="✓ Selesai", bg="white", fg="#10b981",
                     font=("Segoe UI", 9, "bold")).pack(side="left")

        if task.get("description"):
            tk.Label(inner, text=task["description"], bg="white", fg="#6b7280",
                     font=("Segoe UI", 9), anchor="w", justify="left",
                     wraplength=700).pack(fill="x", pady=(4, 0))

        if task["subtasks"]:
            st_frame = tk.Frame(inner, bg="#f9fafb", padx=8, pady=6)
            st_frame.pack(fill="x", pady=(6, 0))
            done_count = sum(1 for s in task["subtasks"] if s["done"])
            tk.Label(st_frame, text=f"Sub-tugas ({done_count}/{len(task['subtasks'])})",
                     bg="#f9fafb", fg="#6b7280",
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")
            for st in task["subtasks"]:
                st_row = tk.Frame(st_frame, bg="#f9fafb")
                st_row.pack(fill="x")
                v = tk.BooleanVar(value=st["done"])
                tk.Checkbutton(st_row, variable=v, bg="#f9fafb", activebackground="#f9fafb",
                               command=lambda tid=task["id"], sid=st["id"]:
                                   self.toggle_subtask(tid, sid)).pack(side="left")
                lbl = tk.Label(st_row, text=st["text"], bg="#f9fafb", anchor="w",
                               fg="#9ca3af" if st["done"] else "#1f2333",
                               font=("Segoe UI", 9))
                lbl.pack(side="left", fill="x", expand=True)
                if st["done"]:
                    lbl.config(font=("Segoe UI", 9, "overstrike"))

        tk.Button(inner, text="+ Sub-tugas",
                  command=lambda: self.add_subtask_to_task(task["id"]),
                  bg="white", fg="#6366f1", relief="flat",
                  font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 0))

    def update_stats(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t["done"])
        active = total - done
        late = sum(1 for t in self.tasks if is_overdue(t))
        self.stat_vars["total"].set(str(total))
        self.stat_vars["done"].set(str(done))
        self.stat_vars["active"].set(str(active))
        self.stat_vars["late"].set(str(late))

    # -------------------------------------------------
    # EXPORT / IMPORT
    # -------------------------------------------------
    def export_data(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile=f"taskmaster-backup-{date.today()}.json"
        )
        if not path:
            return
        data = {"tasks": self.tasks, "exported_at": datetime.now().isoformat()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("Sukses", f"Data berhasil diekspor ke:\n{path}")

    def import_data(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "tasks" not in data or not isinstance(data["tasks"], list):
                raise ValueError("Format file tidak valid")
            if not messagebox.askyesno("Konfirmasi",
                "Import akan MENGGANTI data saat ini. Lanjutkan?"):
                return
            self.tasks = data["tasks"]
            self.save_and_refresh()
            messagebox.showinfo("Sukses", f"Berhasil import {len(self.tasks)} tugas!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal import: {e}")

    # -------------------------------------------------
    # SAVE + REFRESH
    # -------------------------------------------------
    def save_and_refresh(self):
        Storage.save({"tasks": self.tasks})
        self.refresh_tasks()


# =====================================================
# ENTRY POINT
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskMasterApp(root)
    root.mainloop()
