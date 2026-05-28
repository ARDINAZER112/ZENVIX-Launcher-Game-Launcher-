import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import subprocess
import sys
import shutil
import hashlib

# ----------------------------------------------------------------------
# Deteksi mode distribusi (PyInstaller)
# ----------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(APP_DIR, "games.json")
ICONS_DIR = os.path.join(APP_DIR, "icons")
ICON_SIZE = 32

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class GameLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("// ZENVIX Launcher")
        
        # Jendela dibuat agak melebar khas Launcher Game Premium
        window_width = 850
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(650, 450)

        os.makedirs(ICONS_DIR, exist_ok=True)

        self.games = []
        self.filtered_indices = None
        self.selected_index = None
        self.icon_cache = {}

        # ------------------------------------------------------------------
        # PALETTE WARNA THEME
        # ------------------------------------------------------------------
        self.bg_dark = "#111214"       
        self.bg_panel = "#1b1c1f"      
        self.accent_yellow = "#dfff00"  
        self.text_light = "#f5f6f7"     
        self.text_muted = "#7e8494"     

        self.style = ttk.Style()
        if 'clam' in self.style.theme_names():
            self.style.theme_use('clam')
            
        self.configure_styles()
        self.load_games()

        self.root.configure(bg=self.bg_dark)

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ==========================================
        # 1. HEADER AREA (Pencarian / Search)
        # ==========================================
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(search_frame, text="SEARCH //", font=("Segoe UI", 10, "bold"), foreground=self.accent_yellow).pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, ipady=4, padx=(0, 5))
        
        ttk.Button(search_frame, text="CARI", command=self.search_games).pack(side=tk.LEFT, padx=2)
        ttk.Button(search_frame, text="RESET", command=self.reset_search).pack(side=tk.LEFT, padx=2)
        self.search_entry.bind("<Return>", lambda event: self.search_games())

        ttk.Label(search_frame, text="ZENVIX Launcher", font=("Segoe UI", 8), foreground=self.text_muted).pack(side=tk.RIGHT, pady=5)

        # ==========================================
        # 2. MAIN AREA (Daftar Game / Treeview)
        # ==========================================
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("name", "index"),
            show="tree headings",
            selectmode="browse"
        )
        self.tree.heading("#0", text="")
        self.tree.heading("name", text=" DATA INSTALLED KOLEKSI GAME", anchor=tk.W)
        self.tree.heading("index", text="")
        self.tree.column("#0", width=55, anchor=tk.CENTER, stretch=False)
        self.tree.column("name", width=300, anchor=tk.W)
        self.tree.column("index", width=0, stretch=False)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # ==========================================
        # 3. FOOTER AREA (Tombol Aksi Kontrol)
        # ==========================================
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="➕ TAMBAH", command=self.add_game_dialog).pack(side=tk.LEFT, padx=(0, 4), ipady=2)
        ttk.Button(btn_frame, text="✏️ EDIT", command=self.edit_game_dialog).pack(side=tk.LEFT, padx=4, ipady=2)
        ttk.Button(btn_frame, text="❌ HAPUS", command=self.delete_game, style="Danger.TButton").pack(side=tk.LEFT, padx=4, ipady=2)
        ttk.Button(btn_frame, text="📁 PINDAI FOLDER", command=self.scan_directory).pack(side=tk.LEFT, padx=4, ipady=2)
        ttk.Button(btn_frame, text="🔄 REFRESH", command=self.refresh_tree).pack(side=tk.LEFT, padx=4, ipady=2)
        
        ttk.Button(btn_frame, text="🚀 JALANKAN GAME", command=self.run_game, style="Run.TButton").pack(side=tk.RIGHT, ipady=6, ipadx=15)

        self.refresh_tree()

    def configure_styles(self):
        """Mengonfigurasi elemen grafis TTK."""
        self.style.configure(".", background=self.bg_dark, foreground=self.text_light, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.bg_dark)
        self.style.configure("TLabel", background=self.bg_dark, foreground=self.text_light)
        
        self.style.configure("TButton", background="#222429", foreground=self.text_light, borderwidth=0, focuscolor=self.bg_dark, relief="flat")
        self.style.map("TButton", background=[('active', "#2f323a"), ('pressed', self.bg_dark)])
        
        self.style.configure("Run.TButton", background=self.accent_yellow, foreground="#000000", font=("Segoe UI", 10, "bold"), borderwidth=0, relief="flat")
        self.style.map("Run.TButton", background=[('active', "#bacc00"), ('pressed', "#94a300")], foreground=[('active', "#000000")])
        
        self.style.configure("Danger.TButton", background="#3a1c20", foreground="#ff6b6b", borderwidth=0, relief="flat")
        self.style.map("Danger.TButton", background=[('active', "#522429")])
        
        self.style.configure("TEntry", fieldbackground=self.bg_panel, foreground=self.text_light, insertcolor=self.text_light, bordercolor="#2d3035", lightcolor="#2d3035", darkcolor="#2d3035", relief="flat")
        
        self.style.configure("Treeview", background=self.bg_panel, fieldbackground=self.bg_panel, foreground=self.text_light, rowheight=42, borderwidth=0, relief="flat")
        self.style.configure("Treeview.Heading", background="#1e2024", foreground=self.accent_yellow, font=("Segoe UI", 9, "bold"), borderwidth=0, relief="flat")
        self.style.map("Treeview", background=[('selected', "#2d3139")], foreground=[('selected', self.accent_yellow)])

    # ==================================================================
    # DATA
    # ==================================================================
    def load_games(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    self.games = data
                else:
                    self.games = data.get("games", [])
            except:
                self.games = []
        else:
            self.games = []

    def save_games(self):
        data = {"games": self.games}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ==================================================================
    # MANAJEMEN IKON
    # ==================================================================
    def _copy_icon_to_local(self, original_path, game_name):
        if not os.path.isfile(original_path):
            return ""

        name_part = "".join(c for c in game_name if c.isalnum() or c in (' ', '_', '-')).strip()
        if not name_part:
            name_part = "game"
        name_part = name_part.replace(' ', '_')[:30]

        ext = os.path.splitext(original_path)[1].lower()
        if ext not in ('.png', '.jpg', '.jpeg', '.ico', '.bmp'):
            ext = '.png'

        if os.path.abspath(os.path.dirname(original_path)) == os.path.abspath(ICONS_DIR):
            return original_path

        hash_short = hashlib.md5(original_path.encode()).hexdigest()[:8]
        dest_name = f"{name_part}_{hash_short}{ext}"
        dest_path = os.path.join(ICONS_DIR, dest_name)

        if not os.path.exists(dest_path):
            try:
                shutil.copy2(original_path, dest_path)
            except Exception as e:
                print(f"Gagal menyalin ikon: {e}")
                return ""
        return dest_path

    def _load_image_from_file(self, path):
        if not PIL_AVAILABLE:
            return None
        try:
            img = Image.open(path)
            img = img.resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def _get_icon_for_game(self, idx, game):
        if idx in self.icon_cache:
            return self.icon_cache[idx]

        icon_path = game.get("icon", "")
        if icon_path and os.path.isfile(icon_path):
            img = self._load_image_from_file(icon_path)
            if img:
                self.icon_cache[idx] = img
                return img

        exe_path = game.get("path", "")
        if exe_path and os.path.isfile(exe_path):
            folder = os.path.dirname(exe_path)
            base = os.path.splitext(os.path.basename(exe_path))[0]
            candidates = []
            for ext in ('.png', '.jpg', '.jpeg', '.ico', '.bmp'):
                candidates.append(os.path.join(folder, base + ext))
            for ext in ('.png', '.jpg', '.jpeg', '.ico', '.bmp'):
                candidates.append(os.path.join(folder, 'icon' + ext))
            for candidate in candidates:
                if os.path.isfile(candidate):
                    new_icon_path = self._copy_icon_to_local(candidate, game.get("name", ""))
                    if new_icon_path:
                        game["icon"] = new_icon_path
                        self.save_games()
                        img = self._load_image_from_file(new_icon_path)
                        if img:
                            self.icon_cache[idx] = img
                            return img

        self.icon_cache[idx] = ''
        return ''

    # ==================================================================
    # TREEVIEW
    # ==================================================================
    def refresh_tree(self):
        self.filtered_indices = None
        self.search_entry.delete(0, tk.END)
        indices = list(range(len(self.games)))
        self._populate_tree(indices)

    def _populate_tree(self, indices):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.icon_cache.clear()

        for idx in indices:
            if idx >= len(self.games):
                continue
            game = self.games[idx]
            name = game.get("name", "Unnamed")
            display_name = f"  {name}"
            if sys.platform != "win32" and game.get("use_wine", False):
                display_name = "  [WINE] " + name

            icon = self._get_icon_for_game(idx, game)
            self.tree.insert("", tk.END, text="", image=icon, values=(display_name, idx))

    def on_tree_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            if values and len(values) >= 2:
                try:
                    self.selected_index = int(values[1])
                except ValueError:
                    self.selected_index = None
        else:
            self.selected_index = None

    # ==================================================================
    # PENCARIAN
    # ==================================================================
    def search_games(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            self.refresh_tree()
            return
        matched = [i for i, g in enumerate(self.games) if keyword in g.get("name", "").lower()]
        self.filtered_indices = matched
        self._populate_tree(matched)

    def reset_search(self):
        self.refresh_tree()

    # ==================================================================
    # AKSI
    # ==================================================================
    def run_game(self):
        if self.selected_index is None:
            messagebox.showwarning("Pilih Game", "Silakan pilih game terlebih dahulu.")
            return

        game = self.games[self.selected_index]
        executable = game.get("path", "")
        args = game.get("args", "")

        if not executable or not os.path.isfile(executable):
            messagebox.showerror("File Tidak Ditemukan", f"File eksekutor tidak ditemukan:\n{executable}")
            return

        use_wine = game.get("use_wine", False) and sys.platform != "win32"

        try:
            if use_wine:
                if not shutil.which("wine"):
                    messagebox.showerror("Wine Tidak Ditemukan",
                                         "Wine tidak terinstal atau tidak ada di PATH.\n"
                                         "Silakan instal Wine terlebih dahulu.")
                    return
                cmd = ["wine", executable]
            else:
                cmd = [executable]

            if args:
                cmd.extend(args.split())

            subprocess.Popen(cmd, cwd=os.path.dirname(executable))
        except Exception as e:
            messagebox.showerror("Gagal Menjalankan", str(e))

    # -------------------- Dialog Tambah/Edit --------------------
    def add_game_dialog(self):
        self._game_dialog(is_edit=False)

    def edit_game_dialog(self):
        if self.selected_index is None:
            messagebox.showwarning("Pilih Game", "Pilih game yang akan diedit.")
            return
        self._game_dialog(is_edit=True, index=self.selected_index)

    def _game_dialog(self, is_edit=False, index=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("CONFIGURATION // Tambah Game" if not is_edit else "CONFIGURATION // Edit Game")
        
        dialog_width = 620
        dialog_height = 360
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog_width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog_height // 2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        dialog.configure(bg=self.bg_dark)
        dialog.resizable(False, False)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        name_var = tk.StringVar()
        path_var = tk.StringVar()
        args_var = tk.StringVar()
        icon_var = tk.StringVar()
        use_wine_var = tk.BooleanVar(value=False)

        if is_edit and index is not None:
            game = self.games[index]
            name_var.set(game.get("name", ""))
            path_var.set(game.get("path", ""))
            args_var.set(game.get("args", ""))
            icon_var.set(game.get("icon", ""))
            use_wine_var.set(game.get("use_wine", False))

        ttk.Label(frame, text="Nama Game:", foreground=self.text_muted).grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(frame, textvariable=name_var, width=35).grid(row=0, column=1, padx=8, pady=8, ipady=3, sticky=tk.W)

        ttk.Label(frame, text="Lokasi File:", foreground=self.text_muted).grid(row=1, column=0, sticky=tk.W, pady=8)
        ttk.Entry(frame, textvariable=path_var, width=35).grid(row=1, column=1, padx=8, pady=8, ipady=3, sticky=tk.W)
        ttk.Button(frame, text="CARI...",
                command=lambda: self._browse_file(dialog, path_var, name_var, icon_var, use_wine_var)
                ).grid(row=1, column=2, padx=5, sticky=tk.W)

        ttk.Label(frame, text="Argumen Run:", foreground=self.text_muted).grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(frame, textvariable=args_var, width=35).grid(row=2, column=1, padx=8, pady=8, ipady=3, sticky=tk.W)

        ttk.Label(frame, text="Ikon (Path):", foreground=self.text_muted).grid(row=3, column=0, sticky=tk.W, pady=8)
        ttk.Entry(frame, textvariable=icon_var, width=35).grid(row=3, column=1, padx=8, pady=8, ipady=3, sticky=tk.W)
        ttk.Button(frame, text="CARI...",
                command=lambda: self._browse_icon(dialog, icon_var, name_var.get())
                ).grid(row=3, column=2, padx=5, sticky=tk.W)

        if sys.platform != "win32":
            style_check = ttk.Style()
            style_check.configure("TCheckbutton", background=self.bg_dark, foreground=self.accent_yellow)
            ttk.Checkbutton(frame, text="Jalankan Menggunakan Wine Windows Layer", variable=use_wine_var, style="TCheckbutton").grid(row=4, column=1, sticky=tk.W, pady=8)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=3, pady=20)

        def simpan():
            nama = name_var.get().strip()
            path = path_var.get().strip()
            if not nama or not path:
                messagebox.showwarning("Data Kurang", "Nama dan lokasi file harus diisi.", parent=dialog)
                return

            icon_src = icon_var.get().strip()
            if icon_src and os.path.isfile(icon_src):
                new_icon = self._copy_icon_to_local(icon_src, nama)
                if new_icon:
                    icon_var.set(new_icon)

            game_data = {
                "name": nama,
                "path": path,
                "args": args_var.get().strip(),
                "icon": icon_var.get().strip(),
                "use_wine": use_wine_var.get()
            }
            if is_edit and index is not None:
                self.games[index] = game_data
            else:
                self.games.append(game_data)
            self.save_games()
            self.refresh_tree()
            dialog.destroy()

        ttk.Button(btn_frame, text="SIMPAN DATA", style="Run.TButton", command=simpan).pack(side=tk.LEFT, padx=10, ipady=3, ipadx=5)
        ttk.Button(btn_frame, text="BATALKAN", command=dialog.destroy).pack(side=tk.LEFT, padx=10, ipady=3, ipadx=5)

    def _browse_file(self, parent_window, path_var, name_var, icon_var, use_wine_var):
        if sys.platform == "win32":
            filetypes = [("Executable / Installer", "*.exe;*.msi;*.bat;*.cmd;*.com"),
                         ("All files", "*.*")]
        else:
            filetypes = [("All files", "*")]
            
        filename = filedialog.askopenfilename(parent=parent_window, title="Pilih File Game", filetypes=filetypes)
        if not filename:
            return

        path_var.set(filename)

        if not name_var.get().strip():
            base = os.path.splitext(os.path.basename(filename))[0]
            name_var.set(base)

        if use_wine_var is not None and sys.platform != "win32":
            use_wine_var.set(filename.lower().endswith(".exe"))

        folder = os.path.dirname(filename)
        base = os.path.splitext(os.path.basename(filename))[0]
        candidates = []
        for ext in ('.png', '.jpg', '.jpeg', '.ico', '.bmp'):
            candidates.append(os.path.join(folder, base + ext))
        for ext in ('.png', '.jpg', '.jpeg', '.ico', '.bmp'):
            candidates.append(os.path.join(folder, 'icon' + ext))
        for candidate in candidates:
            if os.path.isfile(candidate):
                game_name = name_var.get().strip() or base
                new_icon = self._copy_icon_to_local(candidate, game_name)
                if new_icon:
                    icon_var.set(new_icon)
                return

    def _browse_icon(self, parent_window, icon_var, game_name=""):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.ico *.bmp"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(parent=parent_window, title="Pilih Ikon", filetypes=filetypes)
        if not filename:
            return
        new_icon = self._copy_icon_to_local(filename, game_name)
        if new_icon:
            icon_var.set(new_icon)
        else:
            icon_var.set(filename)

    def delete_game(self):
        if self.selected_index is None:
            messagebox.showwarning("Pilih Game", "Pilih game yang akan dihapus.")
            return
        if messagebox.askyesno("Konfirmasi Hapus",
                               f"Hapus '{self.games[self.selected_index]['name']}' dari daftar?"):
            del self.games[self.selected_index]
            self.save_games()
            self.refresh_tree()

    # ==================================================================
    # PEMINDAI FOLDER
    # ==================================================================
    def is_executable(self, filepath):
        if sys.platform == "win32":
            ext = os.path.splitext(filepath)[1].lower()
            return ext in ('.exe', '.msi', '.bat', '.cmd', '.com')
        else:
            if not os.path.isfile(filepath):
                return False
            basename = os.path.basename(filepath)
            name, ext = os.path.splitext(basename)
            if ext == '.exe':
                return True
            if ext == '.sh':
                return os.access(filepath, os.X_OK)
            if ext == '':
                return os.access(filepath, os.X_OK)
            return False

    def scan_directory(self):
        directory = filedialog.askdirectory(title="Pilih Folder untuk Dipindai")
        if not directory:
            return

        self.root.config(cursor="watch")
        self.root.update()

        new_games = []
        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    full_path = entry.path
                    if self.is_executable(full_path):
                        if not any(g['path'] == full_path for g in self.games):
                            game_name = os.path.splitext(entry.name)[0] if sys.platform == "win32" else entry.name
                            use_wine = (sys.platform != "win32" and full_path.lower().endswith(".exe"))
                            game_data = {
                                'name': game_name,
                                'path': full_path,
                                'args': '',
                                'icon': '',
                                'use_wine': use_wine
                            }
                            folder = os.path.dirname(full_path)
                            base = os.path.splitext(entry.name)[0]
                            candidates = []
                            for ext in ('.png', '.jpg', '.jpeg', '.ico', '.bmp'):
                                candidates.append(os.path.join(folder, base + ext))
                            for ext in ('.png', '.jpg', '.jpeg', '.ico', '.bmp'):
                                candidates.append(os.path.join(folder, 'icon' + ext))
                            for candidate in candidates:
                                if os.path.isfile(candidate):
                                    new_icon = self._copy_icon_to_local(candidate, game_name)
                                    if new_icon:
                                        game_data['icon'] = new_icon
                                    break
                            new_games.append(game_data)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memindai folder:\n{str(e)}")
        finally:
            self.root.config(cursor="")

        if new_games:
            self.games.extend(new_games)
            self.save_games()
            self.refresh_tree()
            messagebox.showinfo("Pemindaian Selesai",
                                f"{len(new_games)} game baru ditemukan dan ditambahkan.")
        else:
            messagebox.showinfo("Pemindaian Selesai", "Tidak ada game baru yang ditemukan.")

# ======================================================================
# JALANKAN APPLICATIONS
# ======================================================================
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure("Treeview", rowheight=40)
    app = GameLauncher(root)
    root.mainloop()