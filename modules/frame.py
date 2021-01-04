


class NavbarActive():
    home = False
    table = False
    write = False
    message = False

    def set_home(self):
        self.home = True
    def set_table(self):
        self.table = True
    def set_write(self):
        self.write = True
    def set_message(self):
        self.message = True


def bool2binary(arg):
    if arg:
        return 1
    return 0