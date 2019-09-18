import subprocess
import time
from io import BytesIO
import requests
from appdirs import user_cache_dir
import os
import vfmflathub
import threading
from appdirs import user_data_dir


class Application:

    def __init__(self, flatpak_id, name, description, latest_version, image_url, installed=False):
        self.flatpak_id = flatpak_id
        self.name = name
        self.description = description
        self.latest_version = latest_version
        self.installed = installed
        self.busy = False
        self.progress = -1

        if image_url.startswith("/"):
            self.image_url = "https://flathub.org{}".format(image_url)
        else:
            self.image_url = image_url

    def get_image(self):
        directory = user_cache_dir("vfm", "vaporos")
        filename = os.path.join(directory, self.flatpak_id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.isfile(filename):
            download = requests.get(self.image_url)
            with open(filename, "wb") as writer:
                writer.write(download.content)
                writer.close()
        return filename

    def launch(self):
        subprocess.Popen(["gtk-launch", self.flatpak_id])

    def install(self):
        if not self.busy:
            self.busy = True
        else:
            print("Error: {} is already being installed".format(self.name))
            return False

        if self.installed:
            print("Error: {} is already installed".format(self.name))
            return False
        thread = threading.Thread(target=self.__track_progress, args=(vfmflathub.install(self),))
        thread.start()

    def uninstall(self):
        if not self.busy:
            self.busy = True
        else:
            print("Error: {} is already being uninstalled".format(self.name))
            return False

        if not self.installed:
            print("Error: {} is not installed".format(self.name))
            return False
        thread = threading.Thread(target=self.__track_progress, args=(vfmflathub.uninstall(self),))
        thread.start()

    def __track_progress(self, subprocess):
        if not self.busy or subprocess is None:
            return -1
        buf = BytesIO()
        while subprocess.poll() is None:
            if self.installed:
                time.sleep(1)
                continue
            out = subprocess.stdout.read(1)
            buf.write(out)
            if out in (b'\r', b'\n'):
                for value in buf.getvalue().split():
                    if isinstance(value, bytes):
                        value = value.decode("utf-8")
                    if "%" in value:
                        self.progress = int(value.replace("%",""))
                buf.truncate(0)
        self.installed = (not self.installed)
        self.busy = False
        self.progress = -1

    def __str__(self):
        # This one makes sure there are no non-ascii characters in the string, for python 2 compatibility
        return ''.join([i if ord(i) < 128 else ' ' for i in self.name]).title()

    def __lt__(self, other):
        names = [str(self), str(other)]
        names.sort()
        if names[0] == str(self) and self.installed == other.installed:
            return True
        if self.installed and not other.installed:
            return True
        return False
