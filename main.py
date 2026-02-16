import sys
import os
import time
import re
import json
import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMenu, QTreeWidget, QTreeWidgetItem, 
                               QStyledItemDelegate, QHeaderView, QListWidget, QPushButton, QMessageBox)
from PySide6.QtGui import QPixmap, QDesktopServices, QIcon, QColor
from ui.ui_main import Ui_MainWindow
from PySide6.QtCore import Qt, QUrl, QSize, QByteArray, QThread, Signal, QTimer
from PySide6.QtWidgets import QWidget
from ui.ui_preferences import Ui_Preferences
from PySide6.QtWidgets import QDialog 
from ui.ui_apikey import Ui_APIkeyDialog
import requests
from typing import Optional, Union, List




class LibraryManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        os.makedirs("data", exist_ok=True)
        self.api_key_path = os.path.join("data","api_key.txt")
        self.token_path = os.path.join("data","token.txt")
        self.db_path = os.path.join("data", "db.json")
        self.posters_path = os.path.join("assets","posters")
        os.makedirs(self.posters_path, exist_ok=True)

        header = self.ui.treeWidget.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Interactive) 
        self.ui.searchResults.setColumnWidth(1, 150)
        
        header = self.ui.searchResults.header()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Interactive) 
        self.ui.searchResults.setColumnWidth(1, 150)

        self.ui.fileExplorerListWidget.itemDoubleClicked.connect(self.FE_item_open)


        self.ui.actionAdd_folder.triggered.connect(self.add_folder)
        self.ui.actionClose.triggered.connect(self.close_folder)


        self.pref_win = PreferencesWindow()
        self.api_win = APIKeyWindow()

        self.ui.startScanPushButton.pressed.connect(self.start_scan)
        
        self.ui.actionPreferences.triggered.connect(self.open_preferences)

        self.ui.fileExplorerListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.fileExplorerListWidget.customContextMenuRequested.connect(self.FE_show_context_menu)

        self.ui.treeWidget.itemClicked.connect(lambda: self.render_seriesInfo("treeWidget"))
        self.ui.searchResults.itemClicked.connect(lambda: self.render_seriesInfo("searchResults"))
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.MF_show_context_menu)
        self.ui.treeWidget.sortItems(0, Qt.AscendingOrder)

        self.ui.searchLineEdit.returnPressed.connect(self.start_search)
        self.ui.SearchPushButton.clicked.connect(self.start_search)
        
        self.ui.addSeriesPushButton.clicked.connect(self.add_series)
        
        
        self.ui.searchResults.setIconSize(QSize(96, 96))
        self.ui.searchResults.setWordWrap(True)
        

        self.check_api_key()
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                db = json.load(f)
            self.show_titles(db)
        except Exception as e:
            print(f"Failed to load cache on startup: {e}")
            self.label_notify("Failed to load added series", "error", 5000)
        self.ui.scanProgressBar.setValue(0)

        #self.process_local_db()

    # Adding titles
    def process_local_db(self):
        id_list = list(self.get_series_ids())
        token = self.get_token()



        self.worker = FullCacheWorker(id_list, token, self)
        self.worker.start()

    def get_series_ids(self) -> list:
        tree_widget = self.ui.treeWidget
        count = self.ui.treeWidget.topLevelItemCount()
        id_list = set()
        top_items = [tree_widget.topLevelItem(i) for i in range(tree_widget.topLevelItemCount())]
        for item in top_items:
            tvdb_id = str(str(item.text(1).split("\n")[2]).split("TVDB id: ")[-1]).strip()
            print(tvdb_id)
            id_list.add(tvdb_id)
        return list(id_list)

    def start_search(self):
        title = self.ui.searchLineEdit.text().strip()
        token = self.get_token()
        if token is None:
            if self.update_tvdb_token() == False:
                print("Failed to start search because no token")
                self.show_messagebox("critical", "Failed to get token.\nCheck your API key or internet connection", "Error")
                return
            token = self.get_token()

        
        self.ui.searchResults.clear()
        
        self.worker = SearchWorker(title, token, self)
        self.worker.result_ready.connect(self.add_result_to_ui)
        self.worker.start()

    def add_series(self):
        print("----------------------add_series----------------------")
        token = self.get_token()
        if token is None:
            self.label_notify("Failed to get token", "error", 5000 )
            return
        
        item = self.ui.searchResults.currentItem()
        if not item:
            return
        
        item_info_text = item.text(1)
        lines = item_info_text.split("\n")
        name = item.text(0)
        tvdb_id = None
        if len(lines) > 2 and "TVDB id: " in lines[2]:
            tvdb_id = lines[2].split("TVDB id: ")[1]
        
        if not tvdb_id:
            self.label_notify("Invalid TVDB ID", "error", 5000)
            return

        cache = {}
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
            except:
                pass

        headers = {"Authorization": f"Bearer {token}", "Accept-Language": "eng"}
        params = {"query": tvdb_id, "type": "series", "limit": 1}
        try:
            r = requests.get("https://api4.thetvdb.com/v4/search", headers=headers, params=params)
            results = r.json()
            if results.get("data"):
                for result in results["data"]:
                    name = result.get("translations", {}).get("eng", result.get("name", ""))
                    tvdb_id = result.get("id", "").strip("series-")
                    url = result.get("image_url")
                    
                    status = result.get("status", "Unknown")
                    year = result.get("year", "N/A")
                    cache[name] = {
                            "tvdb_id": result.get("id", None),
                            "last_updated": datetime.datetime.now().isoformat(),
                            "data": result
                        }
                
                with open(self.cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache, f, ensure_ascii=False, indent=4)
                
                self.show_titles(cache)
                self.label_notify(f"Added: {name}", "info", 10000)

            else:
                self.label_notify("Series data not found", "error", 5000)

        except Exception as e:
            print(f"Request error: {e}")
            self.label_notify("Network error", "error", 5000)

            
    def start_scan(self):
        print("----------------------start_scan----------------------")
        key = self.check_api_key()
        token = None
        try: 
            with open(self.token_path, "r") as f:
                token = f.read().strip()
                if token == "":
                    token = None
        except Exception as e:
            print(f"Failed to extract token from file: {e}")
        
        if token is None:
            token = self.update_tvdb_token()
            if token is None:
                print("Failed to get token")
                self.show_messagebox("critical", "Failed to get token.\nCheck your API key or internet connection", "Error")
                return
        
        if not self.show_messagebox("question",
                                "Please ensure that your folders or files are named after the series.\n\nThis process involves a large number of network requests and may take some time depending on your library size.\n\nDo you want to continue?",
                                "Confirmation"):
            return

        self.ui.scanProgressBar.setValue(10)

        titles = self.scan_library()

        if titles is None:
            print("Folder is empty")
            self.label_notify("Empty folder", "info", 5000)
            self.ui.scanProgressBar.setValue(0)
            return
        print(titles)

        self.ui.scanProgressBar.setValue(20)
        titles.sort()

        self.cache_thread = ScanCacheWorker(titles, token, self)
        self.cache_thread.progress_changed.connect(self.ui.scanProgressBar.setValue)
        self.cache_thread.finished.connect(self.on_cache_finished)
        self.cache_thread.start()

    def on_cache_finished(self, id_list: list):
        print("Caching and searching finished")
        token = self.get_token()
        print(id_list)
        self.full_db_thread = FullCacheWorker(id_list, token, self)
        self.full_db_thread.result_ready.connect(self.save_full_db)
        self.full_db_thread.result_ready.connect(self.show_titles)
        self.full_db_thread.start()
        
        self.ui.scanProgressBar.setValue(100)


    def save_full_db(self, db):
        try:
            with open("data/db.json", "w", encoding="utf-8") as f:
                    json.dump(db, f, ensure_ascii=False, indent=4)
            print("Full DB saved")
        except Exception:
            print("Failed to save full DB")


    def scan_library(self) -> list | None:
        print("----------------------scan_library----------------------")
        folder = self.ui.pathLine.text()
        if os.path.isdir(folder):
            IGNORED_EXTS = {'.ttf', '.otf', '.ttc', '.ass', '.srt', '.txt', '.png', '.jpg', '.jpeg', 
                            '.mka', '.ac3', '.rtf', '.parts', '.mkv', '.mp4', '.avi', '.m4a', '.ini'}

            GARBAGE_WORDS = {"rus", "eng", "sub", "sound", "font", "fonts", "signs", "rus sound", "eng sound", 
                            "rus subs", "eng subs", "rus sounds", "eng sounds", "надписи", "bonus", 
                            "extra", "preview", "scans", "scan", "previews", "commentatory", 
                            "bd menu", "bd", "pv", "anilibria", "anidub", "sovetromantica", 
                            "shiza", "anifilm", "animedia", "aniplay", "crunchyroll", "netflix", "anisense",
                            "booklet", "zendos", "eladiel", "zendos & eladiel", "анимевод", 
                            "ryuji", "seiya & axtr25", "trouble & акварелька", "св-дубль", "субтитры", "alvakarp", 
                            "alisma", "getsmart", "ambiente", "rg genshiken", "studioband", "stan warhammer", 
                            "animereactor", "yss шрифты", "powerwar & co", "aniliberty", "get smart group", "opendub", "antravoco", "1080p", "720p", "480p", "x264", "x265", "h264", "h265", "av1", "10bit", "8bit",
                            "bluray", "bdrip", "web-dl", "webrip", "tvrip", "dvdrip", "hdtv",
                            "dual audio", "multi-sub", "aac", "flac", "dts", "ac3",
                            "repack", "remux", "softsubs", "hardsubs", "raw",
                            "vostfr", "ita", "esp", "ger", "jpn", "dub", "multi",
                            "v0", "v1", "v2", "v3",
                            "preview", "promo", "commercial", "teaser", "opening", "ending", "op", "ed",
                            "shinkai", "miyazaki", "makoto", "ghibli",
                            "anidust", "dreamers", "shikimori", "jut su", "yummyani", "smotret-anime", "sa4ko aka kiyoso", "kbm team"}

            STRICT_GARBAGE = {"sub", "subs", "sound", "font", "fonts", "надписи", "sign", "signs", 
                            "bonus", "nc", "nced", "ncop", "extra", "preview", "scans", "scan", 
                            "previews", "commentatory", "bd menu", "bd", "pv", "novel", "шрифты", "полные",
                            "yss полные", "audio", "lostyears", "box", "op", "ed", "ncop", "nced", "ost", 
                            "music", "soundtrack", "covers", "art", "artbook", "wallpapers", "artwork", 
                            "docs", "info", "read me", "specials", "omake", "shorts", "movies", "sp", "clips", "trailer",
                            "sample", "metadata", "extrafiles", "thumbnails", "temp", "cache",
                            "subtitles", "subs_rus", "subs_eng", "scripts", "ass", "srt",
                            "vol", "volume", "folder", "images", "pics", "screenshots", "cd"}
            


            PATTERNS = [
                r'\s+S\d+E\d+.*',                       # S01E01...
                r'\s+\d{1,2}(st|nd|rd|th)?\s+Stage.*',  # 1st Stage, 2nd Stage...
                r'\s+Season\s+\d+.*',                   # Season 1...
                r'\s+Episode\s+\d+.*',                  # Episode 1...
                r'\s+OVA.*',                            # OVA...
                r'\s+TV.*',                             # TV...
                r'\s+S\d+.*',                           # S1, S2...
                r'\s+-\s+\d+.*',                        # - 01...
                r'\s+\d{1,3}$',                         # Numbers in the end
                r'\s+[0-9]{2,3}(?:\s|$).*'              # 2-3 digit numbers in the middle or at the end
            ]

            self.ui.fileExplorerListWidget.clear()
            clean_titles = set()

            for root, dirs, files in os.walk(folder):
                for d in dirs:
                    low_d = d.lower()
                    if any(word in low_d for word in GARBAGE_WORDS) or low_d in STRICT_GARBAGE:
                        continue

                    name = re.sub(r'\[.*?\]|\(.*?\)', '', d)
                    name = name.replace('_', ' ').replace('.', ' ')
                    

                    for p in PATTERNS:
                        name = re.split(p, name, flags=re.IGNORECASE)[0]
                    

                    name = re.sub(r'\s+(?:Season|Stage|S|St|nd|rd|th|Part)\s*\d+$', '', name, flags=re.IGNORECASE)
                    name = re.sub(r'\s+\d+$', '', name) 

                    name = ' '.join(name.split()).strip(" -.")
                    
                    if name.lower() in STRICT_GARBAGE or len(name) < 3:
                        continue

                    if name:
                        clean_titles.add(name)

                for item in files:
                    low_item = item.lower()
                    if any(low_item.endswith(ext) for ext in IGNORED_EXTS): continue
                    
                    name, _ = os.path.splitext(item)
                    name = re.sub(r'\[.*?\]|\(.*?\)', '', name)
                    name = name.replace('.', ' ').replace('_', ' ')

                    for p in PATTERNS:
                        name = re.split(p, name, flags=re.IGNORECASE)[0]


                    name = re.sub(r'\s+(?:Season|Stage|S|St|nd|rd|th|Part)\s*\d+$', '', name, flags=re.IGNORECASE)
                    name = re.sub(r'\s+\d+$', '', name) 

                    name = name.strip(" -.")

                    if name.lower() in STRICT_GARBAGE or len(name) < 3:
                        continue

                    if name:
                        clean_titles.add(name)

            clean_titles.discard('')
            

            return list(clean_titles)
            
        else:
            print("Directory wasn't found")
            self.label_notify("No such folder", "error", 5000)
            return None
            

    # Visual
    def show_titles(self, db: dict):
        print("----------------------show_titles----------------------")
        self.ui.treeWidget.setColumnCount(2)
        self.ui.treeWidget.setHeaderLabels(["Title", "Info"])
        self.ui.treeWidget.setIconSize(QSize(96, 96))
        self.ui.treeWidget.setWordWrap(True)
        
        shown_titles = set()
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            shown_titles.add(int(str(item.text(1).split("\n")[2]).replace("TVDB id: ", "")))

        lang = "eng"
        for i, title in enumerate(db.values()):
            title_id = title.get("id")
            if title_id in shown_titles:
                continue
            name = None

            langs = title.get("nameTranslations") or []

            if lang in langs:
                translations = title.get("translations")
                if translations:
                    nameTranslations = translations.get("nameTranslations")
                    if nameTranslations:
                        for translation in nameTranslations:
                            if translation.get("language") == lang:
                                name = translation.get("name")
                                break
            if not name:
                name = title.get("name", "Unknown")

            item = QTreeWidgetItem([name])

            url = title.get("image")
            pixmap = self.load_poster(url, title_id)
            
            if pixmap:
                item.setIcon(0, QIcon(pixmap))
            else:
                item.setIcon(0, self.create_placeholder_icon())

            status = title.get("status") or {}
            status_name = status.get("name", "N/A")
            
            year = title.get("year", "N/A")

            info_text = f"{year}\n{status_name}\nTVDB id: {title_id}"

            item.setText(1, info_text)
            self.ui.treeWidget.addTopLevelItem(item)

            progress = 90 + int(((i + 1) / len(db)) * 10)
            self.ui.scanProgressBar.setValue(progress)
            count = self.ui.treeWidget.topLevelItemCount()
            self.ui.addedSeriesLabel.setText(f"Added series ({count})")
            shown_titles.add(title_id)
            QApplication.processEvents()
                    

    def load_poster(self, link: str, tvdb_id: int | str) -> QPixmap | None:
        print("----------------------load_poster----------------------")
        file_path = os.path.join(self.posters_path, f"{tvdb_id}.jpg")

        if os.path.exists(file_path):
            return QPixmap(file_path)

        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                
                
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                return pixmap
        except Exception as e:
            print(f"Failed to save picture: {e}")
        
        return None


            

    def create_placeholder_icon(self):
        print("----------------------create_placeholder_icon----------------------")
        pixmap = QPixmap(50, 70)
        pixmap.fill(QColor("blue"))
        return QIcon(pixmap)

    def add_result_to_ui(self, name, info, pixmap):
        title_item = QTreeWidgetItem([name])
        
        if pixmap:
            title_item.setIcon(0, QIcon(pixmap))
        title_item.setText(1, info)
        self.ui.searchResults.addTopLevelItem(title_item)

    def render_seriesInfo(self, widget: str):
        target_view = self.ui.treeWidget if widget == "treeWidget" else self.ui.searchResults
        other_view = self.ui.searchResults if widget == "treeWidget" else self.ui.treeWidget
        
        item = target_view.currentItem()
        
        if not item:
            return

        other_view.blockSignals(True)
        other_view.setCurrentItem(None)
        other_view.blockSignals(False)
        self.current_widget = widget

        full_title = item.text(0)
        item_info_text = item.text(1)

        lines = item_info_text.split("\n")
        year = lines[0] if len(lines) > 0 else "N/A"
        status = lines[1] if len(lines) > 1 else "N/A"
        
        tvdb_id = "N/A"
        if len(lines) > 2 and "TVDB id: " in lines[2]:
            tvdb_id = lines[2].split("TVDB id: ")[1]


        icon = item.icon(0)
        if not icon.isNull():
            pixmap = icon.pixmap(icon.actualSize(QSize(680, 1000)))
            
            scaled_pixmap = pixmap.scaled(
                self.ui.posterLabel.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.ui.posterLabel.setAlignment(Qt.AlignCenter)
            self.ui.posterLabel.setScaledContents(False)
            self.ui.posterLabel.setPixmap(scaled_pixmap)
        

        self.ui.titleLabel.setText(full_title)
        self.ui.yearLabel.setText(year)
        self.ui.statusLabel.setText(status)
        # self.ui.idLabel.setText(f"TVDB id: {tvdb_id}")

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, 'current_widget') and self.current_widget:
            self.render_seriesInfo(self.current_widget)

    def FE_show_context_menu(self, pos):
        print(f"----------------------FE_show_context_menu----------------------")

        global_pos = self.ui.fileExplorerListWidget.mapToGlobal(pos)
        menu = QMenu(self)
        action1 = menu.addAction("Open in explorer")
        

        action = menu.exec(global_pos)
        
        if action == action1:
            folder_path = self.ui.pathLine.text()
            if os.path.exists(folder_path):

                os.startfile(folder_path)

    def MF_show_context_menu(self, pos):
        print(f"----------------------MF_show_context_menu----------------------")

        global_pos = self.ui.treeWidget.mapToGlobal(pos)
        menu = QMenu(self)
        action1 = menu.addAction("View on TVDB")
        action2 = menu.addAction("Remove from series list")
        
        action = menu.exec(global_pos)
        
        if action == action1:
            item = self.ui.treeWidget.currentItem()
            if item:
                info_text = item.text(1)
                tvdb_id = str(str(info_text.split("\n")[2]).split("TVDB id: ")[1])
                url = QUrl(f"https://www.thetvdb.com/search?query={tvdb_id}")
                QDesktopServices.openUrl(url)
        elif action == action2:
            pass
        
    def show_messagebox(self, m_type: str, text: str, title: str ="Message") -> None | bool:
        if m_type.lower() not in ("information", "warning", "critical", "question"):
            raise ValueError(f"Unknown message type: {m_type}")
        
        msg = QMessageBox(self)
        if m_type == "information":
            msg.setIcon(QMessageBox.Information)
        elif m_type == "warning":
            msg.setIcon(QMessageBox.Warning)
        elif m_type == "critical":
            msg.setIcon(QMessageBox.Critical)
        elif m_type == "question":
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setWindowTitle(title)
        msg.setText(text)
        result = msg.exec()

        return result in (QMessageBox.Yes, QMessageBox.Ok)

    def label_notify(self, text: str, m_type: str = "info", delay: int = 5000):
        color = "red" if m_type == "error" else "black"

        self.ui.statusBarLabel.setStyleSheet(f"color: {color};")
        self.ui.statusBarLabel.setText(text)

        QTimer.singleShot(delay, lambda: self.ui.statusBarLabel.setText(""))

    def open_preferences(self):
        print("----------------------open_preferences----------------------")
        self.pref_win.show()
        self.check_api_key()

    # API key
    def check_api_key(self) -> bool:
        print("----------------------check_api_key----------------------")
        if not os.path.exists(self.api_key_path):
            self.prompt_for_key()
        else:
            with open(self.api_key_path, "r") as f:
                key = f.read().strip()
                if not key:
                    self.label_notify("API key found", "info", 1000)
                    self.prompt_for_key()
                else:
                    self.label_notify("API key found", "info", 1000)
                    return True

    def prompt_for_key(self) -> bool:
        print("----------------------prompt_for_key----------------------")
        if self.api_win.exec(): 
            print("API key found and saved")
            return True
        else:
            print("API key wasn't entered")
            return False

    def request_api_key(self):
        print("----------------------request_api_key----------------------")
        result = self.api_win.exec() 
        if result == QDialog.Accepted:
            print("User updated their API key")
            
    def get_api_key(self) -> str | None:
        print("----------------------get_api_key----------------------")
        try:
            with open(self.api_key_path, "r") as f:
                api_key = f.read()
                return api_key
        except Exception as e:
            print(f"Failed to get API key from file: {e}")
            return None
        
    # Token
    def update_tvdb_token(self) -> bool:
        print("----------------------update_tvdb_token----------------------")
        url = "https://api4.thetvdb.com/v4/login"
        
        try:
            with open(self.api_key_path, "r") as f:
                api_key = f.read()
        except Exception as e:
            print(f"Failed to get API key from file: {e}")
            return False

        payload = {
            "apikey": api_key
        }
        
        try:
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                token = data['data']['token']
                print("Token acquired!")
                self.label_notify("Token acquired", "info", 500)
                try:
                    with open(self.token_path, "w") as f:
                        f.write(token)
                        print("Тoken successfully saved")
                        self.label_notify("Token saved", "info", 1000)
                        return True
                except Exception as e:
                    print(f"Failed to save token: {e}")
                    self.label_notify("Failed to save token", "error", 5000)
                    return False
                        
            else:
                print(f"Auth error: {response.status_code}")
                self.label_notify(f"Auth error: {response.status_code}", "error", 5000)
                print(response.text)
                return False
                
        except Exception as e:
            print(f"Failed to contact the server: {e}")
            self.label_notify("Failed to contact the server", "error", 5000)
            return False
            
    def get_token(self) -> str | None:
        try:
            
            with open(self.token_path, "r") as f:
                token = f.read()
                return token
        except Exception as e:
            print(f"Failed to get token from file: {e}")
            return None
        
    # Files
    def update_files(self):
        print("----------------------update_files----------------------")
        
        folder = self.ui.pathLine.text()
        if os.path.isdir(folder):
            self.ui.fileExplorerListWidget.clear()
            files = os.listdir(folder)
            self.ui.fileExplorerListWidget.addItems(files)
            self.ui.scanProgressBar.setValue(0)
        else:
            self.ui.pathLine.setText("Path not found")


    def add_folder(self):
        print("----------------------add_folder----------------------")
        folder = QFileDialog.getExistingDirectory(self, "Select a library folder")
        if folder:
            self.ui.pathLine.setText(folder)


    def close_folder(self):
        print("----------------------close_folder----------------------")

        self.ui.pathLine.setText("")
        self.ui.fileExplorerListWidget.clear()

    def FE_item_open(self, item):
        print("----------------------FE_item_open----------------------")
        current_item = self.ui.fileExplorerListWidget.currentItem()
        if current_item:
            file_name = current_item.text()
            folder_path = self.ui.pathLine.text()
            

            full_path = os.path.join(folder_path, file_name)
            
            QDesktopServices.openUrl(QUrl.fromLocalFile(full_path))


class PreferencesWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Preferences()
        self.ui.setupUi(self)
        self.api_key_path = os.path.join("data","api_key.txt")
        self.token_path = os.path.join("data","token.txt")
        self.cache_path = os.path.join("data", "dbcache.json")
        self.db_path = os.path.join("data", "db.json")
        self.posters_path = os.path.join("assets","posters")
        self.check_api_key()

    def check_api_key(self):
        if not os.path.exists(self.api_key_path):
            pass
        else:
            with open(self.api_key_path, "r") as f:
                key = f.read().strip()
                if not key:
                    self.ui.P1LineEdit.setPlaceholderText("Enter your API key")
                else:
                    self.ui.P1LineEdit.setText(key)

class APIKeyWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_APIkeyDialog()
        self.ui.setupUi(self)
        self.api_key_path = os.path.join("data","api_key.txt")
        self.token_path = os.path.join("data","token.txt")
        self.cache_path = os.path.join("data", "dbcache.json")
        self.db_path = os.path.join("data", "db.json")
        self.posters_path = os.path.join("assets","posters")
        self.ui.buttonBox.clicked.connect(self.save_and_close)

    def save_and_close(self):
        key = self.ui.APIkeyLineEdit.text().strip()
        
        if key:
            with open(self.api_key_path, "w") as f:
                f.write(key)
            
            self.accept()
        else:
            self.ui.APIkeyLineEdit.setText("")
            self.ui.APIkeyLineEdit.setPlaceholderText("Enter your API key")


class SearchWorker(QThread):
    result_ready = Signal(str, str, object) 

    def __init__(self, title, token, parent_class):
        super().__init__()
        self.title = title
        self.token = token
        self.parent_class = parent_class

    def run(self):
        headers = {"Authorization": f"Bearer {self.token}", "Accept-Language": "eng"}
        params = {"query": self.title, "type": "series", "limit": 10}
        
        try:
            r = requests.get("https://api4.thetvdb.com/v4/search", headers=headers, params=params)
            results = r.json()
            if results.get("data"):
                for result in results["data"]:
                    name = result.get("translations", {}).get("eng", result.get("name", ""))
                    tvdb_id = result.get("id", "").strip("series-")
                    url = result.get("image_url")
                    
                    pixmap = self.parent_class.load_poster(url, tvdb_id)
                    
                    status = result.get("status", "Unknown")
                    year = result.get("year", "N/A")
                    info = f"{year}\n{status}\nTVDB id: {tvdb_id}"
                    

                    self.result_ready.emit(name, info, pixmap)
        except Exception as e:
            print(f"Thread error: {e}")

class ScanCacheWorker(QThread):
    progress_changed = Signal(int)
    finished = Signal(list)
    def __init__(self, titles, token, parent_class):
        super().__init__()
        self.titles = titles
        self.token = token
        self.parent_class = parent_class
        self.cache_path = os.path.join("data", "dbcache.json")
        self.db_path = os.path.join("data", "db.json")
        

    def run(self):
        print("----------------------ScanCacheWorker----------------------")
        path = self.cache_path
        
        cache = {}
        id_list = set()
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cache = json.load(f)
            except json.JSONDecodeError:
                print("Cache file is corrupted")

        headers = {"Authorization": f"Bearer {self.token}"}
        FAKE_WORDS = {"abridged", "parody", "fan", "dub", "re-cut", "fandub"}

        for i, title in enumerate(self.titles):
            if title not in cache:
                cache[title] = {"tvdb_id": None}
            
            tvdb_id = cache[title].get("tvdb_id")
            
            if tvdb_id:
                print(f"From cache: {title} -> {tvdb_id}")
                id_list.add(tvdb_id)
            else:
                print(f"Searching in TVDB: {title}")
                params = {
                    "query": title,
                    "type": "series",
                    "limit": 5 
                }

                try:
                    response = requests.get("https://api4.thetvdb.com/v4/search", headers=headers, params=params, timeout=10)
                    results = response.json()
                    
                    # Errors
                    if response.status_code == 401:
                        print("API Error: 401.\nCheck your API key")
                        self.parent_class.show_messagebox("critical", "API Error: 401.\nCheck your API key", "Error")
                        return
                    elif response.status_code != 200:
                        print(f"API Error: {response.status_code}")
                        self.parent_class.show_messagebox("critical", f"API Error: {response.status_code}", "Error")
                        return
                    
                    best_match = None
                    
                    if results.get("data"):
                        for candidate in results["data"]:
                            name_low = candidate.get("name", "").lower()
                            
                            is_fake = any(fake in name_low for fake in FAKE_WORDS)
                            
                            if not is_fake:
                                best_match = candidate
                                break
                        
                        if not best_match:
                            best_match = results["data"][0]

                    if best_match:
                        tvdb_id = int(str(best_match["id"].split("series-")[-1]).strip())
                        id_list.add(str(tvdb_id))

                    cache[title]["tvdb_id"] = tvdb_id or None
                    time.sleep(0.2) 

                except Exception as e:
                    print(f"Request error for {title}: {e}")
                    self.parent_class.label_notify("Request error", "error", 1000)

            progress = 20 + int(((i + 1) / len(self.titles)) * 70)
            self.progress_changed.emit(progress)
            QApplication.processEvents()
            
            

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Failed to save cache: {e}")
        self.finished.emit(list(id_list))

class FullCacheWorker(QThread):
    result_ready = Signal(dict) 

    def __init__(self, id_list: list, token: str, parent_class):
        super().__init__()
        self.id_list = id_list
        self.token = token
        self.parent_class = parent_class
        self.db_path = os.path.join("data", "db.json")

    def run(self):
        print("----------------------FullCacheWorker----------------------")
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"meta": "translations,episodes"}
        db = {}
        lang = "eng"
        saved_titles = set()
        

        if os.path.exists(self.db_path) and os.path.getsize(self.db_path) > 0:
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    db = json.load(f)
            except json.JSONDecodeError:
                print("DB file is corrupted")
        
            for title_id in db:
                saved_titles.add(str(title_id))

        for tvdb_id in self.id_list:
            tid = str(tvdb_id).strip()
            if tid in saved_titles:
                print(f"{tid} is already saved")
                continue

            
            print(f"Getting full data for {tid}...")

            try:
                r = requests.get(f"https://api4.thetvdb.com/v4/series/{tid}/extended", headers=headers, params=params)
                # Translated episodes data
                r2 = requests.get(f"https://api4.thetvdb.com/v4/series/{tid}/episodes/official/{lang}", headers=headers)
                
                # Errors
                if r.status_code == 401 or r2.status_code == 401:
                    print("API Error: 401.\nCheck your API key")
                    return
                elif r.status_code != 200 or r2.status_code != 200:
                    print(f"API Error: {r.status_code}")
                    return
                
                results = r.json()
                results2 = r2.json()

                original_eps = results.get("data", {}).get("episodes", [])
                translated_data = results2.get("data", {})
                translated_eps = translated_data.get("episodes", [])

                if "data" in results and results["data"]:
                    db[tid] = results["data"]
                    
                    if "data" in results2 and "episodes" in results2["data"]:
                        db[tid]["episodes"] = translated_eps

                        for i in range(len(db[tid]["episodes"])):
                            if db[tid]["episodes"][i].get("name") is None:
                                if i < len(original_eps):
                                    db[tid]["episodes"][i] = original_eps[i]
                            
                            current_ep = db[tid]["episodes"][i]
                            img_path = current_ep.get("image")

                            if img_path and not str(img_path).startswith("http"):
                                current_ep["image"] = f'https://artworks.thetvdb.com{img_path}'
                
                print(f"Successfully got full data for {tid} - {db.get(tid).get("name")}")
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(0.2) 
        self.result_ready.emit(db)
        self.finished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryManager()
    window.show()
    sys.exit(app.exec())