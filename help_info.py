import tkinter as tk
from tkinter import messagebox

def pokaz_okno_o_programie():
    """
    Wyświetla okno dialogowe z informacją o programie
    """
    messagebox.showinfo("O programie", "Program do sprawdzania wersji Windows.\nAutor: Tomek")

def pokaz_okno_pomoc():
    """
    Wyświetla okno dialogowe z instrukcją obsługi
    """
    instrukcja = (
        "Instrukcja obsługi programu:\n\n"
        "1. Wybierz dysk z listy.\n"
        "2. Kliknij 'Sprawdź', aby rozpocząć analizę.\n"
        "3. Po zakończeniu kliknij 'Zapisz raport', aby wyeksportować wyniki.\n\n"
        "Powodzenia!"
    )
    messagebox.showinfo("Pomoc", instrukcja)

def dodaj_menu_pomocy(pomoc_menu: tk.Menu):
    """
    Dodaje opcje do menu 'Pomoc'
    """
    pomoc_menu.add_command(label="O programie", command=pokaz_okno_o_programie)
    pomoc_menu.add_command(label="Pomoc", command=pokaz_okno_pomoc)
    pomoc_menu.add_command(label="Sprawdź aktualizacje",
                           command=lambda: messagebox.showinfo("Aktualizacja", "Brak dostępnych aktualizacji."))
    pomoc_menu.add_command(label="Zgłoś błąd",
                           command=lambda: messagebox.showinfo("Zgłoszenie błędu", "Dziękujemy za zgłoszenie błędu."))
