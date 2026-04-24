# Project: Inventory Tracking and Management System
# Author: Ali Zubair Shah
# GitHub: https://github.com/K3rNel1

import customtkinter as ctk
import os
import ctypes
from datetime import datetime, timedelta
from Backend import (
    is_first_run, create_user, verify_login, change_password, get_username,
    issue_book, get_all_records, get_record, get_record_by_id, update_record, update_record_by_id, delete_record,
    get_duplicate_records, delete_duplicate_records, delete_record_by_id,
    get_overdue_records, is_overdue,
    generate_default_message, send_whatsapp_message,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_DARK        = "#0f1117"
SIDEBAR_BG     = "#161b22"
CARD_BG        = "#1c2128"
CARD_HOVER     = "#252c35"
ACCENT         = "#58a6ff"
ACCENT_HOVER   = "#79bbff"
SUCCESS        = "#3fb950"
DANGER         = "#f85149"
WARNING        = "#d29922"
WARNING_BG     = "#2d2000"
WARNING_BORDER = "#6e4c00"
TEXT_PRIMARY   = "#e6edf3"
TEXT_SECONDARY = "#8b949e"
BORDER         = "#30363d"
ENTRY_BG       = "#21262d"

ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a.ico")


def _set_icon(window):
    if os.path.exists(ICON_PATH):
        try:
            window.iconbitmap(ICON_PATH)
        except Exception:
            pass


class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Register — Login")
        self.geometry("440x520")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)
        _set_icon(self)

        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        except Exception:
            pass

        self.authenticated = False
        self._failed_attempts = 0

        self.after(200, lambda: _set_icon(self))

        if is_first_run():
            self._build_setup_ui()
        else:
            self._build_login_ui()

    def _build_setup_ui(self):
        self._clear()
        card = self._center_card(460)

        ctk.CTkLabel(card, text="📚", font=ctk.CTkFont(size=48)).pack(pady=(10, 0))
        ctk.CTkLabel(card, text="Create Your Account",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(pady=(6, 2))
        ctk.CTkLabel(card, text="Set up a username and password to protect the register.",
                     font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY,
                     wraplength=320).pack(pady=(0, 20))

        self._user_entry  = self._field(card, "Username")
        self._pass_entry  = self._field(card, "Password", show="●")
        self._pass2_entry = self._field(card, "Confirm Password", show="●")

        self._err_label = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12),
                                       text_color=DANGER)
        self._err_label.pack(pady=(4, 0))

        ctk.CTkButton(card, text="Create Account", height=40, corner_radius=8,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self._do_setup).pack(fill="x", pady=(10, 0))

        self.bind("<Return>", lambda e: self._do_setup())

    def _do_setup(self):
        username = self._user_entry.get().strip()
        password = self._pass_entry.get()
        confirm  = self._pass2_entry.get()

        if not username:
            self._err_label.configure(text="Username cannot be empty.")
            return
        if len(password) < 4:
            self._err_label.configure(text="Password must be at least 4 characters.")
            return
        if password != confirm:
            self._err_label.configure(text="Passwords do not match.")
            return

        create_user(username, password)
        self._err_label.configure(text="")
        self._build_login_ui(welcome=True)

    def _build_login_ui(self, welcome=False):
        self._clear()
        card = self._center_card(420)

        ctk.CTkLabel(card, text="📚", font=ctk.CTkFont(size=48)).pack(pady=(10, 0))
        ctk.CTkLabel(card, text="Library Register",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(pady=(4, 2))

        if welcome:
            ctk.CTkLabel(card, text="Account created! Please log in.",
                         font=ctk.CTkFont(size=12), text_color=SUCCESS).pack(pady=(0, 16))
        else:
            ctk.CTkLabel(card, text="Sign in to continue",
                         font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY).pack(pady=(0, 16))

        self._user_entry = self._field(card, "Username")
        self._pass_entry = self._field(card, "Password", show="●")

        self._err_label = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12),
                                       text_color=DANGER)
        self._err_label.pack(pady=(4, 0))

        ctk.CTkButton(card, text="Login", height=40, corner_radius=8,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=self._do_login).pack(fill="x", pady=(10, 0))

        self.bind("<Return>", lambda e: self._do_login())

    def _do_login(self):
        username = self._user_entry.get()
        password = self._pass_entry.get()

        if verify_login(username, password):
            self.authenticated = True
            self.destroy()
        else:
            self._failed_attempts += 1
            remaining = 3 - self._failed_attempts
            if remaining > 0:
                self._err_label.configure(
                    text=f"Invalid credentials. {remaining} attempt(s) remaining."
                )
                self._pass_entry.delete(0, "end")
            else:
                self._err_label.configure(text="Too many failed attempts.")
                self.after(1500, self.destroy)

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _center_card(self, height):
        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")
        card = ctk.CTkFrame(outer, fg_color=CARD_BG, corner_radius=16,
                            border_width=1, border_color=BORDER, width=360)
        card.pack(padx=20, pady=20)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=36, pady=32, fill="both", expand=True)
        return inner

    def _field(self, parent, label, show=None):
        ctk.CTkLabel(parent, text=label,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_SECONDARY).pack(anchor="w", pady=(8, 2))
        kwargs = dict(height=36, corner_radius=8, fg_color=ENTRY_BG,
                      border_color=BORDER, border_width=1,
                      text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=13))
        if show:
            kwargs["show"] = show
        entry = ctk.CTkEntry(parent, **kwargs)
        entry.pack(fill="x")
        return entry


class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        except Exception:
            pass

        self.title("Library Register")
        self.geometry("1050x660")
        self.minsize(900, 580)
        self.configure(fg_color=BG_DARK)
        self.after(200, lambda: _set_icon(self))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()
        self._show_issue_page()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color=SIDEBAR_BG)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        title_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(28, 4))

        ctk.CTkLabel(title_frame, text="📚", font=ctk.CTkFont(size=32)).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Library",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Register",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=ACCENT).pack(anchor="w")

        ctk.CTkFrame(self.sidebar, height=1, fg_color=BORDER).pack(fill="x", padx=20, pady=(20, 20))

        self.nav_buttons = {}
        self.nav_buttons["issue"]    = self._sidebar_button("📝  Issue Book",    self._show_issue_page)
        self.nav_buttons["register"] = self._sidebar_button("📖  View Register", self._show_register_page)

        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(fill="both", expand=True)

        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.pack(fill="x", padx=16, pady=(0, 6))

        ctk.CTkLabel(user_frame, text=f"👤  {get_username()}",
                     font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w")

        ctk.CTkButton(user_frame, text="🔑  Change Password", anchor="w",
                      font=ctk.CTkFont(size=12),
                      fg_color="transparent", text_color=TEXT_SECONDARY,
                      hover_color=CARD_BG, height=30, corner_radius=6,
                      command=self._open_change_password).pack(fill="x", pady=(4, 0))

        ctk.CTkLabel(self.sidebar, text="© Ali Zubair Shah • K3rNel",
                     font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY).pack(
                         side="bottom", pady=(0, 18))

    def _sidebar_button(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar, text=text, anchor="w",
            font=ctk.CTkFont(size=14),
            fg_color="transparent", text_color=TEXT_SECONDARY,
            hover_color=CARD_BG, height=42, corner_radius=8,
            command=command
        )
        btn.pack(fill="x", padx=14, pady=3)
        return btn

    def _set_active_nav(self, key):
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=ACCENT, text_color="#ffffff", hover_color=ACCENT_HOVER)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_SECONDARY, hover_color=CARD_BG)

    def _build_content_area(self):
        self.content = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _show_issue_page(self):
        self._set_active_nav("issue")
        self._clear_content()

        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        card = ctk.CTkFrame(wrapper, fg_color=CARD_BG, corner_radius=16,
                            border_width=1, border_color=BORDER)
        card.pack(padx=40, pady=30)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=40, pady=36)

        ctk.CTkLabel(inner, text="Issue a Book",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=TEXT_PRIMARY).grid(row=0, column=0, columnspan=2,
                                                   sticky="w", pady=(0, 4))
        ctk.CTkLabel(inner, text="Fill in the details below to register a new book issue.",
                     font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY).grid(
                         row=1, column=0, columnspan=2, sticky="w", pady=(0, 20))

        fields = {}
        labels = [
            ("Book Name",      "bname"),
            ("Borrower Name",  "name"),
            ("Contact Number", "mob"),
            ("Date of Issue",  "doi"),
            ("Date of Return", "dor"),
            ("Remarks",        "rm"),
        ]

        today_str  = datetime.now().strftime("%d-%m-%Y")
        return_str = (datetime.now() + timedelta(days=1)).strftime("%d-%m-%Y")
        defaults   = {"doi": today_str, "dor": return_str}

        for i, (label_text, key) in enumerate(labels):
            row = i + 2
            ctk.CTkLabel(inner, text=label_text,
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=TEXT_SECONDARY).grid(row=row, column=0, sticky="w",
                                                          pady=(8, 2), padx=(0, 20))
            entry = ctk.CTkEntry(inner, width=320, height=38, corner_radius=8,
                                 fg_color=ENTRY_BG, border_color=BORDER, border_width=1,
                                 text_color=TEXT_PRIMARY,
                                 placeholder_text_color=TEXT_SECONDARY,
                                 font=ctk.CTkFont(size=13))
            entry.grid(row=row, column=1, sticky="ew", pady=(8, 2))
            if key in defaults:
                entry.insert(0, defaults[key])
            fields[key] = entry

        def submit():
            bname = fields["bname"].get().strip()
            name  = fields["name"].get().strip()
            mob   = fields["mob"].get().strip()
            doi   = fields["doi"].get().strip()
            dor   = fields["dor"].get().strip()
            rm    = fields["rm"].get().strip()

            if not bname or not name or not mob or not doi or not dor:
                self._toast("Please fill in all required fields.", DANGER)
                return
            try:
                int(mob)
            except ValueError:
                self._toast("Contact number must be a valid number.", DANGER)
                return

            try:
                duplicates = get_duplicate_records(name, mob)
            except Exception as e:
                self._toast(f"Database error: {e}", DANGER)
                return

            def _do_insert():
                try:
                    issue_book(bname, name, mob, doi, dor, rm)
                except Exception as e:
                    self._toast(f"Database error: {e}", DANGER)
                    return
                self._toast(f"Book \"{bname}\" issued to {name} ✓", SUCCESS)
                for key, entry in fields.items():
                    entry.delete(0, "end")
                fields["doi"].insert(0, today_str)
                fields["dor"].insert(0, return_str)
                fields["bname"].focus()

            def _on_replace(row_id):
                delete_record_by_id(row_id)
                _do_insert()

            if duplicates:
                self._show_duplicate_popup(
                    duplicates=duplicates,
                    on_replace=_on_replace,
                    on_add_anyway=_do_insert,
                )
            else:
                _do_insert()

        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.grid(row=len(labels) + 2, column=0, columnspan=2,
                       sticky="e", pady=(22, 0))
        ctk.CTkButton(btn_frame, text="  Issue Book  ", height=40, corner_radius=8,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      command=submit).pack(side="right")

    def _show_register_page(self):
        self._set_active_nav("register")
        self._clear_content()

        top = ctk.CTkFrame(self.content, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(28, 14))

        ctk.CTkLabel(top, text="Register",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(side="left")

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._render_records())

        ctk.CTkEntry(top, textvariable=self.search_var,
                     placeholder_text="🔍  Search by book or borrower…",
                     width=280, height=36, corner_radius=8,
                     fg_color=ENTRY_BG, border_color=BORDER, border_width=1,
                     text_color=TEXT_PRIMARY,
                     font=ctk.CTkFont(size=13)).pack(side="right")

        ctk.CTkButton(top, text="↻ Refresh", width=90, height=36, corner_radius=8,
                      fg_color=CARD_BG, hover_color=CARD_HOVER, border_width=1,
                      border_color=BORDER, text_color=TEXT_SECONDARY,
                      font=ctk.CTkFont(size=13),
                      command=self._render_records).pack(side="right", padx=(0, 10))

        self.scroll = ctk.CTkScrollableFrame(
            self.content, fg_color="transparent", corner_radius=0,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=TEXT_SECONDARY
        )
        self.scroll.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        self.scroll.grid_columnconfigure(0, weight=1)

        self._render_records()

    def _render_records(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        rows  = get_all_records()
        query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""

        if query:
            rows = [r for r in rows if query in r[1].lower() or query in r[2].lower()]

        if not rows:
            empty = ctk.CTkFrame(self.scroll, fg_color="transparent")
            empty.pack(fill="both", expand=True, pady=80)
            ctk.CTkLabel(empty, text="📭", font=ctk.CTkFont(size=48)).pack()
            ctk.CTkLabel(empty,
                         text="No records found" if query else "Register is empty",
                         font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=TEXT_SECONDARY).pack(pady=(10, 4))
            ctk.CTkLabel(empty,
                         text="Issue a book to see it here." if not query else "Try a different search term.",
                         font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY).pack()
            return

        overdue_list = get_overdue_records()
        if overdue_list:
            banner = ctk.CTkFrame(self.scroll, fg_color=WARNING_BG, corner_radius=10,
                                  border_width=1, border_color=WARNING_BORDER)
            banner.pack(fill="x", pady=(0, 10))
            banner_inner = ctk.CTkFrame(banner, fg_color="transparent")
            banner_inner.pack(fill="x", padx=16, pady=10)

            ctk.CTkLabel(banner_inner,
                         text=f"⚠️  {len(overdue_list)} overdue return{'s' if len(overdue_list) != 1 else ''}",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=WARNING).pack(side="left")

            ctk.CTkLabel(banner_inner,
                         text="Overdue records are highlighted below.",
                         font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(
                             side="left", padx=(10, 0))

        header = ctk.CTkFrame(self.scroll, fg_color=SIDEBAR_BG,
                              corner_radius=10, height=40)
        header.pack(fill="x", pady=(0, 6))
        header.pack_propagate(False)
        header_inner = ctk.CTkFrame(header, fg_color="transparent")
        header_inner.pack(fill="x", padx=16, pady=8)

        col_widths = [
            ("Book", 0.22), ("Borrower", 0.18), ("Contact", 0.14),
            ("Issued", 0.13), ("Return", 0.13), ("Remarks", 0.10), ("", 0.10)
        ]
        for text, w in col_widths:
            ctk.CTkLabel(header_inner, text=text,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=TEXT_SECONDARY,
                         width=int(w * 700)).pack(side="left", padx=2)

        for row_id, bname, name, mob, doi, dor, rm in rows:
            self._record_card(row_id, bname, name, mob, doi, dor, rm)

        ctk.CTkLabel(self.scroll,
                     text=f"  {len(rows)} record{'s' if len(rows) != 1 else ''} found",
                     font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(
                         anchor="w", pady=(8, 0))

    def _record_card(self, row_id, bname, name, mob, doi, dor, rm):
        overdue      = is_overdue(dor)
        card_color   = WARNING_BG if overdue else CARD_BG
        border_color = WARNING_BORDER if overdue else BORDER

        card = ctk.CTkFrame(self.scroll, fg_color=card_color, corner_radius=10,
                            border_width=1, border_color=border_color, height=46)
        card.pack(fill="x", pady=3)
        card.pack_propagate(False)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=10)

        col_data = [
            (str(bname), 0.22), (str(name), 0.18), (str(mob), 0.14),
            (str(doi), 0.13), (str(dor), 0.13), (str(rm or "—"), 0.10)
        ]
        for text, w in col_data:
            ctk.CTkLabel(inner, text=text, font=ctk.CTkFont(size=13),
                         text_color=WARNING if overdue else TEXT_PRIMARY,
                         width=int(w * 700), anchor="w").pack(side="left", padx=2)

        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(side="right")

        if overdue:
            ctk.CTkButton(
                btn_frame, text="💬", width=32, height=28, corner_radius=6,
                fg_color="transparent", hover_color="#1a3d1a",
                text_color=SUCCESS, font=ctk.CTkFont(size=14),
                command=lambda i=row_id: self._open_whatsapp_dialog(i)
            ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame, text="✎", width=32, height=28, corner_radius=6,
            fg_color="transparent", hover_color=ENTRY_BG,
            text_color=ACCENT, font=ctk.CTkFont(size=15),
            command=lambda i=row_id: self._open_edit_dialog(i)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            btn_frame, text="🗑", width=32, height=28, corner_radius=6,
            fg_color="transparent", hover_color="#3d1f1f",
            text_color=DANGER, font=ctk.CTkFont(size=14),
            command=lambda i=row_id: self._confirm_delete(i)
        ).pack(side="left", padx=2)

    def _show_duplicate_popup(self, duplicates, on_replace, on_add_anyway):
        FIELD_LABELS = [
            ("\U0001f4d6  Book Name",      0),
            ("\U0001f464  Borrower Name",  1),
            ("\U0001f4de  Mobile",         2),
            ("\U0001f4c5  Date of Issue",  3),
            ("\U0001f501  Date of Return", 4),
            ("\U0001f4ac  Remarks",        5),
        ]

        popup = ctk.CTkToplevel(self)
        popup.title("Existing Entry Found")
        popup.geometry("520x500")
        popup.minsize(480, 420)
        popup.resizable(False, False)
        popup.configure(fg_color=BG_DARK)
        popup.grab_set()
        popup.focus()
        popup.after(200, lambda: _set_icon(popup))

        popup.update_idletasks()
        sw = popup.winfo_screenwidth()
        sh = popup.winfo_screenheight()
        popup.geometry(f"520x500+{(sw - 520) // 2}+{(sh - 500) // 2}")

        container = ctk.CTkFrame(popup, fg_color="transparent")
        container.pack(fill="both", expand=True)

        def _clear_container():
            for w in container.winfo_children():
                w.destroy()

        def _make_card():
            card = ctk.CTkFrame(container, fg_color=CARD_BG, corner_radius=16,
                                border_width=1, border_color=WARNING_BORDER)
            card.pack(fill="both", expand=True, padx=20, pady=20)
            card.grid_rowconfigure(2, weight=1)
            card.grid_columnconfigure(0, weight=1)
            return card

        def _entry_block(parent, idx, row_data, show_select_hint=False):
            row_id, bname, name, mob, doi, dor, rm = row_data
            values = [bname, name, str(mob), doi, dor, rm or "\u2014"]

            ef = ctk.CTkFrame(parent, fg_color=WARNING_BG, corner_radius=10,
                              border_width=1, border_color=WARNING_BORDER)
            ef.pack(fill="x", pady=(0, 8))

            inner = ctk.CTkFrame(ef, fg_color="transparent")
            inner.pack(fill="x", padx=16, pady=12)

            hdr = ctk.CTkFrame(inner, fg_color="transparent")
            hdr.pack(fill="x", pady=(0, 6))
            ctk.CTkLabel(hdr, text=f"Entry {idx + 1}",
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=WARNING).pack(side="left")
            if show_select_hint:
                ctk.CTkLabel(hdr, text="\u2190 click to select",
                             font=ctk.CTkFont(size=11),
                             text_color=TEXT_SECONDARY).pack(side="right")

            for lbl, col_idx in FIELD_LABELS:
                rf = ctk.CTkFrame(inner, fg_color="transparent")
                rf.pack(fill="x", pady=2)
                ctk.CTkLabel(rf, text=lbl,
                             font=ctk.CTkFont(size=12, weight="bold"),
                             text_color=TEXT_SECONDARY,
                             width=150, anchor="w").pack(side="left")
                ctk.CTkLabel(rf, text=values[col_idx],
                             font=ctk.CTkFont(size=12),
                             text_color=TEXT_PRIMARY,
                             anchor="w").pack(side="left", padx=(8, 0))

            return ef, inner, hdr

        def _show_screen1():
            _clear_container()
            card = _make_card()

            hdr = ctk.CTkFrame(card, fg_color="transparent")
            hdr.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 0))

            ctk.CTkLabel(hdr, text="\u26a0\ufe0f  Existing Entry Found",
                         font=ctk.CTkFont(size=18, weight="bold"),
                         text_color=WARNING).pack(anchor="w")
            msg = ("An existing entry already exists with this borrower name."
                   if len(duplicates) == 1 else
                   f"{len(duplicates)} existing entries found with this borrower name.")
            ctk.CTkLabel(hdr, text=msg, font=ctk.CTkFont(size=12),
                         text_color=TEXT_SECONDARY, justify="left").pack(anchor="w", pady=(6, 0))

            ctk.CTkFrame(card, height=1, fg_color=BORDER).grid(
                row=1, column=0, sticky="ew", padx=20, pady=(14, 0))

            scroll = ctk.CTkScrollableFrame(card, fg_color="transparent", corner_radius=0,
                                            scrollbar_button_color=BORDER,
                                            scrollbar_button_hover_color=TEXT_SECONDARY)
            scroll.grid(row=2, column=0, sticky="nsew", padx=16, pady=(10, 0))

            for idx, row_data in enumerate(duplicates):
                _entry_block(scroll, idx, row_data, show_select_hint=False)

            ctk.CTkFrame(card, height=1, fg_color=BORDER).grid(
                row=3, column=0, sticky="ew", padx=20, pady=(8, 0))

            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.grid(row=4, column=0, sticky="ew", padx=24, pady=(12, 20))

            ctk.CTkButton(btn_row, text="Cancel", width=100, height=36, corner_radius=8,
                          fg_color=ENTRY_BG, hover_color="#3d1f1f",
                          text_color=DANGER, border_width=1, border_color=DANGER,
                          font=ctk.CTkFont(size=13),
                          command=popup.destroy).pack(side="left")

            def _replace_clicked():
                if len(duplicates) == 1:
                    popup.destroy()
                    on_replace(duplicates[0][0])
                else:
                    _show_screen2()

            ctk.CTkButton(btn_row, text="Replace Entry", width=130, height=36, corner_radius=8,
                          fg_color=WARNING_BG, hover_color="#3d2800",
                          text_color=WARNING, border_width=1, border_color=WARNING_BORDER,
                          font=ctk.CTkFont(size=13, weight="bold"),
                          command=_replace_clicked).pack(side="left", padx=(10, 0))

            ctk.CTkButton(btn_row, text="Add Anyway", width=120, height=36, corner_radius=8,
                          fg_color="#1a3d1a", hover_color="#2ea043",
                          text_color=SUCCESS, border_width=1, border_color=SUCCESS,
                          font=ctk.CTkFont(size=13, weight="bold"),
                          command=lambda: (popup.destroy(), on_add_anyway())
                          ).pack(side="right")

        def _show_screen2():
            _clear_container()
            card = _make_card()

            hdr = ctk.CTkFrame(card, fg_color="transparent")
            hdr.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 0))

            ctk.CTkLabel(hdr, text="\U0001f501  Select Entry to Replace",
                         font=ctk.CTkFont(size=18, weight="bold"),
                         text_color=WARNING).pack(anchor="w")
            ctk.CTkLabel(hdr, text="Click on the entry you want to replace with the new record.",
                         font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY,
                         justify="left").pack(anchor="w", pady=(6, 0))

            ctk.CTkFrame(card, height=1, fg_color=BORDER).grid(
                row=1, column=0, sticky="ew", padx=20, pady=(14, 0))

            scroll = ctk.CTkScrollableFrame(card, fg_color="transparent", corner_radius=0,
                                            scrollbar_button_color=BORDER,
                                            scrollbar_button_hover_color=TEXT_SECONDARY)
            scroll.grid(row=2, column=0, sticky="nsew", padx=16, pady=(10, 0))

            selected_id  = ctk.IntVar(value=-1)
            entry_frames = {}

            def _select(row_id):
                selected_id.set(row_id)
                for rid, frm in entry_frames.items():
                    if rid == row_id:
                        frm.configure(fg_color="#1a3a1a", border_color=SUCCESS)
                    else:
                        frm.configure(fg_color=WARNING_BG, border_color=WARNING_BORDER)
                confirm_btn.configure(state="normal",
                                      fg_color="#1a3d1a", hover_color="#2ea043",
                                      text_color=SUCCESS, border_color=SUCCESS)

            for idx, row_data in enumerate(duplicates):
                row_id = row_data[0]
                ef, inner, hdr_frame = _entry_block(scroll, idx, row_data, show_select_hint=True)
                entry_frames[row_id] = ef

                _rid = row_id
                for widget in ef.winfo_children() + [ef]:
                    try:
                        widget.bind("<Button-1>", lambda e, r=_rid: _select(r))
                    except Exception:
                        pass
                for widget in inner.winfo_children() + [inner]:
                    try:
                        widget.bind("<Button-1>", lambda e, r=_rid: _select(r))
                    except Exception:
                        pass

            ctk.CTkFrame(card, height=1, fg_color=BORDER).grid(
                row=3, column=0, sticky="ew", padx=20, pady=(8, 0))

            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.grid(row=4, column=0, sticky="ew", padx=24, pady=(12, 20))

            ctk.CTkButton(btn_row, text="\u2190 Back", width=90, height=36, corner_radius=8,
                          fg_color=ENTRY_BG, hover_color=CARD_HOVER,
                          text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=13),
                          command=_show_screen1).pack(side="left")

            ctk.CTkButton(btn_row, text="Cancel", width=90, height=36, corner_radius=8,
                          fg_color=ENTRY_BG, hover_color="#3d1f1f",
                          text_color=DANGER, border_width=1, border_color=DANGER,
                          font=ctk.CTkFont(size=13),
                          command=popup.destroy).pack(side="left", padx=(8, 0))

            def _confirm_replace():
                row_id = selected_id.get()
                if row_id == -1:
                    return
                popup.destroy()
                on_replace(row_id)

            confirm_btn = ctk.CTkButton(
                btn_row, text="\u2713  Replace Selected",
                width=160, height=36, corner_radius=8,
                fg_color=ENTRY_BG, hover_color=ENTRY_BG,
                text_color=TEXT_SECONDARY, border_width=1, border_color=BORDER,
                font=ctk.CTkFont(size=13, weight="bold"),
                state="disabled",
                command=_confirm_replace
            )
            confirm_btn.pack(side="right")

        _show_screen1()

    def _open_whatsapp_dialog(self, row_id):
        rec = get_record_by_id(row_id)
        if not rec:
            self._toast("Record not found.", DANGER)
            return

        _rec_id, bname, name, mob, doi, dor, rm = rec

        try:
            from Backend import _parse_date
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            due   = _parse_date(dor).replace(hour=0, minute=0, second=0, microsecond=0)
            days_overdue = max((today - due).days, 0)
        except Exception:
            days_overdue = 0

        default_msg = generate_default_message(name, bname, dor, days_overdue)

        dialog = ctk.CTkToplevel(self)
        dialog.title("Send WhatsApp Reminder")
        dialog.geometry("520x560")
        dialog.resizable(False, False)
        dialog.configure(fg_color=BG_DARK)
        dialog.grab_set()
        dialog.focus()
        dialog.after(200, lambda: _set_icon(dialog))

        card = ctk.CTkFrame(dialog, fg_color=CARD_BG, corner_radius=16,
                            border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True, padx=24, pady=24)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        ctk.CTkLabel(inner, text="💬  Send WhatsApp Reminder",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w")

        info_frame = ctk.CTkFrame(inner, fg_color=ENTRY_BG, corner_radius=8)
        info_frame.pack(fill="x", pady=(12, 0))
        info_inner = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_inner.pack(fill="x", padx=14, pady=10)

        ctk.CTkLabel(info_inner, text="To:",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_SECONDARY).pack(side="left")
        ctk.CTkLabel(info_inner, text=f"  {name}",
                     font=ctk.CTkFont(size=13), text_color=TEXT_PRIMARY).pack(side="left")
        ctk.CTkLabel(info_inner, text=f"  •  📞 {mob}",
                     font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(side="left")

        overdue_label = "today" if days_overdue == 0 else f"{days_overdue} day(s) ago"
        ctk.CTkLabel(info_inner, text=f"  •  Due: {dor} ({overdue_label})",
                     font=ctk.CTkFont(size=12), text_color=WARNING).pack(side="left")

        ctk.CTkLabel(inner, text="Message (editable)",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=TEXT_SECONDARY).pack(anchor="w", pady=(16, 4))

        msg_box = ctk.CTkTextbox(inner, height=180, corner_radius=8,
                                 fg_color=ENTRY_BG, border_color=BORDER, border_width=1,
                                 text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=13))
        msg_box.pack(fill="x")
        msg_box.insert("0.0", default_msg)

        ctk.CTkButton(inner, text="↺  Reset to default", height=28, corner_radius=6,
                      fg_color="transparent", text_color=TEXT_SECONDARY,
                      hover_color=ENTRY_BG, font=ctk.CTkFont(size=12),
                      command=lambda: (msg_box.delete("0.0", "end"),
                                       msg_box.insert("0.0", default_msg))
                      ).pack(anchor="e", pady=(4, 0))

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x", pady=(14, 0))

        ctk.CTkButton(btn_row, text="Cancel", width=90, height=36, corner_radius=8,
                      fg_color=ENTRY_BG, hover_color=CARD_HOVER,
                      text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=13),
                      command=dialog.destroy).pack(side="left")

        def do_send():
            message = msg_box.get("0.0", "end").strip()
            if not message:
                return
            ok, err = send_whatsapp_message(mob, message)
            if ok:
                self._toast(f"WhatsApp opened for {name} ✓", SUCCESS)
                dialog.destroy()
            else:
                self._toast(f"Failed: {err}", DANGER)

        ctk.CTkButton(btn_row, text="📲  Open in WhatsApp", width=180, height=36,
                      corner_radius=8, fg_color=SUCCESS, hover_color="#2ea043",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=do_send).pack(side="right")

    def _open_edit_dialog(self, row_id):
        _full_row = get_record_by_id(row_id)
        if not _full_row:
            self._toast("Record not found.", DANGER)
            return
        row = list(_full_row[1:])  # strip id → [bname, name, mob, doi, dor, rm]

        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Record")
        dialog.geometry("480x620")
        dialog.resizable(False, False)
        dialog.configure(fg_color=BG_DARK)
        dialog.grab_set()
        dialog.focus()
        _set_icon(dialog)
        dialog.after(200, lambda: _set_icon(dialog))

        card = ctk.CTkFrame(dialog, fg_color=CARD_BG, corner_radius=16,
                            border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True, padx=24, pady=24)

        card.grid_rowconfigure(1, weight=1)
        card.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 0))

        ctk.CTkLabel(header, text="Edit Record",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w")
        ctk.CTkLabel(header, text=f"Editing record for: {row[1]}",
                     font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(
                         anchor="w", pady=(2, 0))

        fields_frame = ctk.CTkFrame(card, fg_color="transparent")
        fields_frame.grid(row=1, column=0, sticky="nsew", padx=28, pady=(16, 0))

        labels  = ["Book Name", "Borrower Name", "Contact", "Date of Issue", "Date of Return", "Remarks"]
        keys    = ["bname", "name", "mob", "doi", "dor", "rm"]
        entries = {}

        for i, (lbl, key) in enumerate(zip(labels, keys)):
            ctk.CTkLabel(fields_frame, text=lbl,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=TEXT_SECONDARY).pack(anchor="w", pady=(8, 1))
            entry = ctk.CTkEntry(fields_frame, height=34, corner_radius=8,
                                 fg_color=ENTRY_BG, border_color=BORDER, border_width=1,
                                 text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=13))
            entry.pack(fill="x")
            entry.insert(0, str(row[i]) if row[i] else "")
            if key == "name":
                entry.configure(state="disabled")
            entries[key] = entry

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(row=2, column=0, sticky="ew", padx=28, pady=(12, 24))

        def save():
            new_bname = entries["bname"].get().strip()
            new_mob   = entries["mob"].get().strip()
            new_doi   = entries["doi"].get().strip()
            new_dor   = entries["dor"].get().strip()
            new_rm    = entries["rm"].get().strip()

            if not new_bname or not new_doi or not new_dor:
                self._toast("Book name, DOI and DOR are required.", DANGER)
                return
            try:
                int(new_mob) if new_mob else 0
            except ValueError:
                self._toast("Contact must be a valid number.", DANGER)
                return
            try:
                update_record_by_id(row_id,
                                    new_bname=new_bname, new_mob=new_mob or None,
                                    new_doi=new_doi, new_dor=new_dor, new_rm=new_rm)
            except Exception as e:
                self._toast(f"Database error: {e}", DANGER)
                return

            self._toast(f"Record for {row[1]} updated ✓", SUCCESS)
            dialog.destroy()
            self._render_records()

        ctk.CTkButton(btn_row, text="Cancel", width=90, height=36, corner_radius=8,
                      fg_color=ENTRY_BG, hover_color=CARD_HOVER,
                      text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=13),
                      command=dialog.destroy).pack(side="left")

        ctk.CTkButton(btn_row, text="Save Changes", width=130, height=36, corner_radius=8,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=save).pack(side="right")

        dialog.bind("<Return>", lambda e: save())

    def _confirm_delete(self, row_id):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirm Delete")
        dialog.geometry("400x220")
        dialog.resizable(False, False)
        dialog.configure(fg_color=BG_DARK)
        dialog.grab_set()
        dialog.focus()
        dialog.after(200, lambda: _set_icon(dialog))

        card = ctk.CTkFrame(dialog, fg_color=CARD_BG, corner_radius=16,
                            border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True, padx=24, pady=24)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        _del_rec  = get_record_by_id(row_id)
        _del_name = _del_rec[2] if _del_rec else "this record"
        _del_book = _del_rec[1] if _del_rec else ""

        ctk.CTkLabel(inner, text="⚠️  Delete Record",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=DANGER).pack(anchor="w")
        ctk.CTkLabel(inner,
                     text=f"Remove \"{_del_book}\" borrowed by {_del_name}?\nThis cannot be undone.",
                     font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY,
                     justify="left").pack(anchor="w", pady=(10, 0))

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x", side="bottom")

        ctk.CTkButton(btn_row, text="Cancel", width=90, height=36, corner_radius=8,
                      fg_color=ENTRY_BG, hover_color=CARD_HOVER,
                      text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=13),
                      command=dialog.destroy).pack(side="left")

        def do_delete():
            try:
                delete_record_by_id(row_id)
            except Exception as e:
                self._toast(f"Database error: {e}", DANGER)
                return
            self._toast(f"Record for {_del_name} removed.", DANGER)
            dialog.destroy()
            self._render_records()

        ctk.CTkButton(btn_row, text="Delete", width=100, height=36, corner_radius=8,
                      fg_color=DANGER, hover_color="#da3633",
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=do_delete).pack(side="right")

    def _open_change_password(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Change Password")
        dialog.geometry("400x360")
        dialog.resizable(False, False)
        dialog.configure(fg_color=BG_DARK)
        dialog.grab_set()
        dialog.focus()
        dialog.after(200, lambda: _set_icon(dialog))

        card = ctk.CTkFrame(dialog, fg_color=CARD_BG, corner_radius=16,
                            border_width=1, border_color=BORDER)
        card.pack(fill="both", expand=True, padx=24, pady=24)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=28, pady=24)

        ctk.CTkLabel(inner, text="🔑  Change Password",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=TEXT_PRIMARY).pack(anchor="w", pady=(0, 16))

        def _lbl(text):
            ctk.CTkLabel(inner, text=text,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=TEXT_SECONDARY).pack(anchor="w", pady=(8, 2))

        def _entry(show=None):
            e = ctk.CTkEntry(inner, height=34, corner_radius=8,
                             fg_color=ENTRY_BG, border_color=BORDER, border_width=1,
                             text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=13),
                             show=show or "")
            e.pack(fill="x")
            return e

        _lbl("Current Password")
        old_entry = _entry(show="●")
        _lbl("New Password")
        new_entry = _entry(show="●")
        _lbl("Confirm New Password")
        cnf_entry = _entry(show="●")

        err_lbl = ctk.CTkLabel(inner, text="", font=ctk.CTkFont(size=12),
                               text_color=DANGER)
        err_lbl.pack(pady=(6, 0))

        def do_change():
            old = old_entry.get()
            new = new_entry.get()
            cnf = cnf_entry.get()

            if len(new) < 4:
                err_lbl.configure(text="New password must be at least 4 characters.")
                return
            if new != cnf:
                err_lbl.configure(text="New passwords do not match.")
                return
            if change_password(get_username(), old, new):
                self._toast("Password changed successfully ✓", SUCCESS)
                dialog.destroy()
            else:
                err_lbl.configure(text="Current password is incorrect.")

        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x", pady=(14, 0))

        ctk.CTkButton(btn_row, text="Cancel", width=90, height=36, corner_radius=8,
                      fg_color=ENTRY_BG, hover_color=CARD_HOVER,
                      text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=13),
                      command=dialog.destroy).pack(side="left")

        ctk.CTkButton(btn_row, text="Update Password", width=140, height=36,
                      corner_radius=8, fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      font=ctk.CTkFont(size=13, weight="bold"),
                      command=do_change).pack(side="right")

        dialog.bind("<Return>", lambda e: do_change())

    def _toast(self, message, colour=ACCENT):
        toast = ctk.CTkFrame(self, fg_color=colour, corner_radius=10, height=42)
        toast.place(relx=0.5, rely=1.0, anchor="s", y=-20)
        toast.lift()
        ctk.CTkLabel(toast, text=f"  {message}  ",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#ffffff").pack(padx=18, pady=9)

        def remove():
            try:
                toast.destroy()
            except Exception:
                pass

        self.after(2800, remove)


if __name__ == "__main__":
    auth = AuthWindow()
    auth.mainloop()

    if auth.authenticated:
        app = LibraryApp()
        app.mainloop()

