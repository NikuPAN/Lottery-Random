import customtkinter as ctk

from .generator import generate_games, Game


MAIN_COUNT = 6  # how many main numbers per game


class LottoApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        # Window config
        self.title("Lotto Generator")
        self.geometry("520x420")
        self.resizable(False, False)

        # Global appearance
        ctk.set_appearance_mode("dark")          # "light" or "dark"
        ctk.set_default_color_theme("blue")      # "blue", "green", "dark-blue"

        # UI layout
        self._build_ui()

    def _build_ui(self) -> None:
        # Root frame
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Title
        title_label = ctk.CTkLabel(
            frame,
            text="Lotto Generator",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(pady=(12, 4))

        self.subtitle_label = ctk.CTkLabel(
            frame,
            text="Generates random 6 main numbers + 1 bonus (1–45 by default).",
            font=ctk.CTkFont(size=12),
        )
        self.subtitle_label.pack(pady=(0, 16))

        # Input area
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=8)

        # Number of games
        count_label = ctk.CTkLabel(
            input_frame,
            text="Number of games:",
            width=130,
            anchor="w",
        )
        count_label.grid(row=0, column=0, padx=(0, 8), pady=4, sticky="w")

        self.count_entry = ctk.CTkEntry(
            input_frame,
            width=80,
            placeholder_text="e.g. 4",
        )
        self.count_entry.insert(0, "4")
        self.count_entry.grid(row=0, column=1, padx=(0, 12), pady=4, sticky="w")

        # Max number (upper bound)
        max_label = ctk.CTkLabel(
            input_frame,
            text="Max number (range 1–N):",
            width=160,
            anchor="w",
        )
        max_label.grid(row=1, column=0, padx=(0, 8), pady=4, sticky="w")

        self.max_entry = ctk.CTkEntry(
            input_frame,
            width=80,
            placeholder_text="45 or 47",
        )
        self.max_entry.insert(0, "45")
        self.max_entry.grid(row=1, column=1, padx=(0, 12), pady=4, sticky="w")

        # Generate button
        generate_button = ctk.CTkButton(
            input_frame,
            text="Generate",
            command=self.on_generate_clicked,
        )
        generate_button.grid(row=0, column=2, rowspan=2, padx=(8, 0), pady=4, sticky="ns")

        # Result area
        self.result_box = ctk.CTkTextbox(
            frame,
            height=200,
            wrap="none",
            font=ctk.CTkFont(size=20)
        )
        self.result_box.pack(fill="both", expand=True, padx=8, pady=(16, 8))

        # Bottom buttons
        bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=8, pady=(4, 0))

        clear_button = ctk.CTkButton(
            bottom_frame,
            text="Clear",
            width=80,
            command=self.clear_results,
        )
        clear_button.pack(side="left")

        copy_button = ctk.CTkButton(
            bottom_frame,
            text="Copy to clipboard",
            command=self.copy_to_clipboard,
        )
        copy_button.pack(side="right")

        # Status label
        self.status_label = ctk.CTkLabel(
            frame,
            text="Ready.",
            anchor="w",
            font=ctk.CTkFont(size=11),
        )
        self.status_label.pack(fill="x", padx=8, pady=(4, 4))

    def on_generate_clicked(self) -> None:
        """Handle the Generate button click."""
        # Parse number of games
        count_raw = self.count_entry.get().strip()
        try:
            count = int(count_raw)
            if count <= 0:
                raise ValueError
        except ValueError:
            self._set_status("Please enter a valid positive integer for number of games.", error=True)
            return

        # Parse max number (upper bound)
        max_raw = self.max_entry.get().strip() or "45"
        try:
            max_number = int(max_raw)
            # need at least MAIN_COUNT + 1 unique numbers
            if max_number < MAIN_COUNT + 1:
                raise ValueError
        except ValueError:
            self._set_status(
                f"Please enter a valid integer ≥ {MAIN_COUNT + 1} for max number.",
                error=True,
            )
            return

        try:
            games = generate_games(count, max_number=max_number, main_count=MAIN_COUNT)
        except Exception as ex:  # noqa: BLE001
            self._set_status(f"Error: {ex}", error=True)
            return

        # Update subtitle to reflect current range
        self.subtitle_label.configure(
            text=f"Generating 6 main + 1 bonus from range 1–{max_number}."
        )

        self.display_games(games)
        self._set_status(f"Generated {len(games)} game(s) with range 1–{max_number}.", error=False)

    def display_games(self, games: list[Game]) -> None:
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")

        for idx, game in enumerate(games, start=1):
            self.result_box.insert(
                "end",
                f"Game {idx:02d}:  {game.format()}\n",
            )

        self.result_box.configure(state="disabled")

    def clear_results(self) -> None:
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.configure(state="disabled")
        self._set_status("Cleared.", error=False)

    def copy_to_clipboard(self) -> None:
        text = self.result_box.get("1.0", "end").strip()
        if not text:
            self._set_status("Nothing to copy.", error=True)
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self._set_status("Copied to clipboard.", error=False)

    def _set_status(self, message: str, error: bool = False) -> None:
        self.status_label.configure(
            text=message,
            text_color="red" if error else "white",
        )


def run_app() -> None:
    """Entry point for running the UI."""
    app = LottoApp()
    app.mainloop()
