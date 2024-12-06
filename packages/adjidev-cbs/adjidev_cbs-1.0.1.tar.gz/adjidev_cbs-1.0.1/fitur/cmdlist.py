import os
import xml.etree.ElementTree as ET
import subprocess
from dataclasses import dataclass
from typing import List, Optional

colors = {
    "red": '\033[31m',
    "green": '\033[32m',
    "yellow": '\033[33m',
    "blue": '\033[34m',
    "magenta": '\033[35m',
    "cyan": '\033[36m',
    "white": '\033[37m',
    "reset": '\033[0m'
}

restricted_cmds = ['rm', 'format', 'shutdown', 'reboot', 'del', 'exec', 'load', 'clear', 'cls']

@dataclass
class Feature:
    name: str
    description: str
    author: str
    execute: str
    args: Optional[str]
    folder_path: str

def MuatFiturDariXml(file_path: str, folder_path: str, loaded_cmds: dict) -> List[Feature]:
    features = []
    if os.path.exists(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        for setting in root.findall('cbs_setting'):
            name = setting.find('cmd').text
            description = setting.find('description').text
            author = setting.find('author').text
            execute = setting.find('execute').text
            args = setting.find('args').text if setting.find('args') is not None else None

            # Mengecek apakah <cmd> mengandung kata yang dilarang
            if any(restricted_word in name for restricted_word in restricted_cmds):
                print(f"{colors['red']}Error: Cmd '{name}' mengandung kata yang dilarang. Dihapus dari daftar.{colors['reset']}")
                continue

            if name in loaded_cmds:
                print(f"{colors['red']}Error: Cmd '{name}' ditemukan di dua file yang berbeda:{colors['reset']}")
                print(f"{colors['yellow']}File Pertama:{colors['reset']} {loaded_cmds[name]}")
                print(f"{colors['yellow']}File Kedua:{colors['reset']} {file_path}")
                continue

            loaded_cmds[name] = file_path

            feature = Feature(name=name, description=description, author=author, execute=execute, args=args, folder_path=folder_path)
            features.append(feature)
    return features

def InisialisasiFolder(base_folder: str) -> List[Feature]:
    all_features = []
    loaded_cmds = {}  # Dictionary untuk menyimpan cmd yang sudah dimuat
    for foldername in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, foldername)
        if os.path.isdir(folder_path):
            xml_file_path = os.path.join(folder_path, 'cbs_config.xml')
            features = MuatFiturDariXml(xml_file_path, folder_path, loaded_cmds)
            all_features.extend(features)
    return all_features

def JalankanPayload(feature: Feature, args: Optional[str] = None) -> None:
    if feature.execute:
        try:
            if feature.args:
                formatted_args = feature.args.format(args=args if args else "")
                command = f"{feature.execute} {formatted_args}".strip()
            else:
                command = feature.execute

            print(f"{colors['green']}Running . . .{colors['reset']}")
            subprocess.run(command, shell=True, check=True, cwd=feature.folder_path)
        except subprocess.CalledProcessError as e:
            pass
        except Exception as e:
            print(f"{colors['red']}Error: {e}{colors['reset']}")

class DaftarFitur:
    @staticmethod
    def Fiturnya() -> str:
        feature_list = f"{colors['yellow']}Options{colors['reset']}:\n"
        features = InisialisasiFolder(os.path.join(os.getcwd(), 'payloads'))
        for feature in features:
            feature_list += f"    {colors['green']}{feature.name}{colors['reset']}  {colors['magenta']}>>{colors['reset']} {feature.description} ({colors['blue']}Author{colors['reset']}: {feature.author})\n"
        return feature_list

    @staticmethod
    def JalankanPerintahFeature(name: str, args: Optional[str] = None) -> None:
        features = InisialisasiFolder(os.path.join(os.getcwd(), 'payloads'))
        for feature in features:
            if feature.name == name:
                JalankanPayload(feature, args=args)
                return
        print(f"\n")
