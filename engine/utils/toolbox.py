"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .settings import Settings

# Python
import os
import datetime
from typing import Any, Dict, List

"""___Classes___________________________________________________________________________________"""


class ToolBox(Settings):

    def write_txt(self, path: str, text: str, append: bool = False) -> None:
        if append:
            method = "a"
        else:
            method = "w"
        if "/" in path:
            SplitPath = path.split("/")
            os.makedirs("/".join(SplitPath[:-1]), exist_ok=True)
        txt = open(f"{path}", method, encoding="utf-8")
        txt.write(text)
        txt.close()

    def read_txt(self, path: str) -> str:
        txt = open(path, "r", encoding="utf-8", errors="ignore")
        data = txt.read()
        txt.close()
        return data

    def export_txt(self, txt: str, title: str = "DebugExport") -> None:
        self.write_txt(f"{title}", txt)

    def print_info(self, text: str, object: Any, brut: bool = False) -> None:
        """
        Print function. Option available : liste -> displays object line by line.
        """
        if brut:
            print(f"{text} : {object}")
            return
        if isinstance(object, list):
            print(f"{text} ({type(object)})\t:")
            for data in object:
                self.print_info(text, data)
        elif isinstance(object, dict):
            print(f"{text} ({type(object)})\t:")
            for key, value in object.items():
                self.print_info(key, value)
        else:
            print(f"{text} ({type(object)})\t: {object}")

    def add_log(self, text: str, objects: Dict[str, Any] = {}, time: bool = True, disp: bool = True) -> None:
        if objects == {}:
            log = f"{text}"
        else:
            log = f"{text} : {objects}"
        if time:
            now = f"[{datetime.datetime.now().strftime("%d/%m/%Y-%H:%M")}]"
            log = f"{now} - {log}"
        self.write_txt(self.paths["file_log"], log + "\n", append=True)
        if disp:
            print(log)

    def del_log(self):
        try:
            os.remove(self.paths["file_log"])
        except FileNotFoundError:
            pass

    def get_local_files(self, path: str) -> List[str]:
        return os.listdir(path)

    def delete(self, path: str) -> None:
        os.remove(path)

    def search_format(self, format: str, path: str) -> list[str]:
        files = []
        lenF = len(format)
        for file in os.listdir(path):
            if os.path.isfile(path + "/" + file):
                if len(file) > lenF and file[-lenF:] == format:
                    files.append(path + "/" + file)
            else:
                files += self.search_format(format, path + "/" + file)
        return files

    def clean_folder(self, path: str, subcall: bool = False) -> None:
        if os.path.exists(path):
            files = os.listdir(path)
            for file in files:
                if "." in file:
                    os.remove(f"{path}/{file}")
                else:
                    self.clean_folder(f"{path}/{file}", subcall=True)
            if subcall:
                os.rmdir(path)
