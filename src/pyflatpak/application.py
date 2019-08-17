import subprocess


class application():

    def __init__(self, id, remote):
        self.__remote = remote
        self.__id = id
        self.description = ""

    def __get_info(self, remote, id):
        command = ["flatpak", "remote-info", "--user", remote, id]
        line_number = 1
        for line in subprocess.check_output(command).splitlines():
            if line_number == 2:
                self.description = line
                break
            line_number += 1
        print(self.description)

    def __str__(self):
        if not self.description:
            self.__get_info(self.__remote, self.__id)
        return self.description
