class Application:

    def __init__(self, flatpak_id, name, description, latest_version, image_url, installed=False):
        self.flatpak_id = flatpak_id
        self.name = name
        self.description = description
        self.latest_version = latest_version
        self.image_url = image_url
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
