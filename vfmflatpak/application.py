import subprocess

class Version():
    UNKNOWN = "unknown"

class application():

    def __init__(self, id, remote, name, installed, description="", version=Version.UNKNOWN):
        self.id = id
        self.remote = remote
        self.name = name
        self.description = description
        self.version = version
        self.installed = installed

        if not self.description:
            self.description = self.id

    def install(self):
        return_value = subprocess.call(["flatpak", "install", "--user", "-y", self.remote, self.id])
        if return_value != 0:
            raise Exception("Error: Failed to install application {}".format(self.id))
        print("{} was successfully installed".format(self.id))
        self.installed = True

    def uninstall(self):
        return_value = subprocess.call(["flatpak", "uninstall", "--user", "-y", self.id])
        if return_value != 0:
            raise Exception("Error: Failed to uninstall application {}".format(self.id))
        print("{} was successfully uninstalled".format(self.id))
        self.installed = False

    def __str__(self):
        return self.name.title()

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        names = [str(self), str(other)]
        names.sort()
        if names[0] == str(self):
            return True
        return False
