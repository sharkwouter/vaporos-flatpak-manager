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

    def install(self):
        return_value = subprocess.call(["flatpak", "install", "--user", "-y", self.remote, self.flatpak_id])
        if return_value != 0:
            raise Exception("Error: Failed to install application {}".format(self.flatpak_id))
        print("{} was successfully installed".format(self.flatpak_id))
        self.installed = True

    def uninstall(self):
        return_value = subprocess.call(["flatpak", "uninstall", "--user", self.flatpak_id])
        if return_value != 0:
            raise Exception("Error: Failed to uninstall application {}".format(self.flatpak_id))
        print("{} was successfully uninstalled".format(self.flatpak_id))
        self.installed = False

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
