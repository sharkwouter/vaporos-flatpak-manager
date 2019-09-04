import subprocess

class Version():
    UNKNOWN = "unknown"

class application():

    def __init__(self, flatpak_id, remote, name, installed, description="", version=Version.UNKNOWN):
        self.flatpak_id = flatpak_id
        self.remote = remote
        self.name = name
        self.description = description
        self.version = version
        self.installed = installed

        if not self.description:
            self.description = self.flatpak_id

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
