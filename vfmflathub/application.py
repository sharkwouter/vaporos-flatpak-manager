import requests
from appdirs import user_cache_dir
import os


class Application:

    def __init__(self, flatpak_id, name, description, latest_version, image_url, installed=False):
        self.flatpak_id = flatpak_id
        self.name = name
        self.description = description
        self.latest_version = latest_version
        self.installed = installed

        if image_url.startswith("/"):
            self.image_url = "https://flathub.org{}".format(image_url)
        else:
            self.image_url = image_url

    def get_image(self):
        directory = user_cache_dir("vfm", "vaporos")
        filename = "{}/{}.png".format(directory, self.flatpak_id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.isfile(filename):
            download = requests.get(self.image_url)
            with open(filename, "wb") as writer:
                writer.write(download.content)
                writer.close()
        return filename

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        names = [str(self), str(other)]
        names.sort()
        if names[0] == str(self) and self.installed == other.installed:
            return True
        if self.installed and not other.installed:
            return True
        return False
