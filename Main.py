import os
import psutil
import wmi
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

KV = '''
<MainScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        MDToolbar:
            title: "Monitor Systemu"
            elevation: 10
            right_action_items: [["theme-light-dark", lambda x: app.open_theme_menu()]]

        MDTabs:
            id: tabs
            on_tab_switch: app.on_tab_switch(*args)

            Tab:
                title: "Ogólne"
                GeneralTab:

            Tab:
                title: "Log"
                LogTab:

<GeneralTab>:
    ScrollView:
        MDGridLayout:
            cols: 1
            adaptive_height: True
            padding: dp(10)
            spacing: dp(10)

<LogTab>:
    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: dp(10)
            spacing: dp(5)

<MenuContent>:
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height

    MDList:
        id: menu_list
'''

class GeneralTab(MDBoxLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

    def update_info(self, system_info):
        self.clear_widgets()
        grid = Builder.load_string("""
MDGridLayout:
    cols: 2
    adaptive_height: True
    spacing: dp(10)
""")
        for key, value in system_info.items():
            label_key = MDLabel(text=f"{key}:", halign="right", font_style="Subtitle1")
            label_value = MDLabel(text=str(value), halign="left", font_style="Body1")
            grid.add_widget(label_key)
            grid.add_widget(label_value)
        self.add_widget(grid)

class LogTab(MDBoxLayout, MDTabsBase):
    log_content = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10

    def update_log(self, log_text):
        self.clear_widgets()
        if not log_text:
            self.add_widget(MDLabel(text="Brak logów do wyświetlenia.", halign="center"))
            return
        for line in log_text.splitlines():
            log_label = MDLabel(text=line, halign="left", size_hint_y=None, height=20, font_style="Caption")
            self.add_widget(log_label)

class MenuContent(MDBoxLayout):
    pass

class MainScreen(MDBoxLayout):
    pass

class SystemMonitorApp(MDApp):
    selected_disk = StringProperty("")
    partitions = ListProperty([])
    dialog = None
    theme_dialog = None

    def build(self):
        self.title = "Monitor Systemu"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        Window.size = (900, 700)
        return Builder.load_string(KV)

    def on_start(self):
        self.get_partitions()
        self.show_partition_selection()

    def get_partitions(self):
        self.partitions = [p.device for p in psutil.disk_partitions()]
        if self.partitions:
            self.selected_disk = self.partitions[0]
        else:
            self.selected_disk = ""

    def show_partition_selection(self):
        if not self.partitions:
            self.show_error("Brak dostępnych dysków.")
            return

        content = MDBoxLayout(orientation='vertical', adaptive_height=True)
        for partition in self.partitions:
            content.add_widget(
                OneLineListItem(
                    text=partition,
                    on_release=lambda x, p=partition: self.set_partition(p)
                )
            )

        self.dialog = MDDialog(
            title="Wybierz dysk",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Anuluj", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def set_partition(self, partition):
        self.selected_disk = partition
        self.dialog.dismiss()
        self.update_system_info()
        self.update_log_content()

    def update_system_info(self):
        system_info = self.collect_system_info()
        general_tab = self.root.ids.tabs.get_tab_list()[0].content
        if isinstance(general_tab, GeneralTab):
            general_tab.update_info(system_info)
        else:
            self.show_error("Nie można zaktualizować zakładki Ogólne.")

    def collect_system_info(self):
        info = {}
        try:
            c = wmi.WMI()
            os_info = c.Win32_OperatingSystem()[0]
            cpu_info = c.Win32_Processor()[0]
            ram_info = psutil.virtual_memory()
            motherboard = c.Win32_BaseBoard()[0]
            bios = c.Win32_BIOS()[0]
            gpu = c.Win32_VideoController()[0]

            info["System Operacyjny"] = os_info.Caption
            info["Wersja OS"] = os_info.Version
            info["CPU"] = cpu_info.Name.strip()
            info["Częstotliwość CPU"] = f"{cpu_info.CurrentClockSpeed} MHz"
            info["RAM"] = f"{ram_info.total / (1024 ** 3):.2f} GB"
            info["Płyta Główna"] = motherboard.Product
            info["BIOS"] = bios.SMBIOSBIOSVersion
            info["GPU"] = gpu.Name
        except Exception as e:
            self.show_error(f"Błąd podczas zbierania informacji: {e}")
        return info

    def update_log_content(self):
        log_path = os.path.join(self.selected_disk, "Windows", "Panther", "setupact.log")
        try:
            if not os.path.exists(log_path):
                raise FileNotFoundError("Plik setupact.log nie istnieje.")
            with open(log_path, 'r', encoding='utf-8') as f:
                log_text = f.read()
        except Exception as e:
            log_text = f"Błąd odczytu logu: {e}"
        log_tab = self.root.ids.tabs.get_tab_list()[1].content
        if isinstance(log_tab, LogTab):
            log_tab.update_log(log_text)
        else:
            self.show_error("Nie można zaktualizować zakładki Log.")

    def show_error(self, message):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Błąd",
            text=message,
            buttons=[
                MDFlatButton(text="Zamknij", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

    def open_theme_menu(self):
        if not self.theme_dialog:
            content = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
            content.height = dp(100)
            content.add_widget(
                OneLineListItem(text="Jasny", on_release=lambda x: self.set_theme("Light"))
            )
            content.add_widget(
                OneLineListItem(text="Ciemny", on_release=lambda x: self.set_theme("Dark"))
            )
            content.add_widget(
                OneLineListItem(text="Srebrny", on_release=lambda x: self.set_theme("Gray"))
            )

            self.theme_dialog = MDDialog(
                title="Wybierz motyw",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Anuluj", on_release=lambda x: self.theme_dialog.dismiss())
                ],
            )
        self.theme_dialog.open()

    def set_theme(self, theme):
        if theme == "Light":
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"
        elif theme == "Dark":
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Blue"
        elif theme == "Gray":
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Gray"
        self.theme_dialog.dismiss()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "Ogólne":
            self.update_system_info()
        elif tab_text == "Log":
            self.update_log_content()

if __name__ == "__main__":
    SystemMonitorApp().run()
