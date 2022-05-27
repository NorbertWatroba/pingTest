class Loco:

    def __init__(self, ip, name, flag=True):
        self.ip_address = ip
        self.name = name
        self.flag = flag

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def name(self):
        return self._name

    @property
    def flag(self):
        return self._flag

    @ip_address.setter
    def ip_address(self, address):
        self._ip_address = address

    @name.setter
    def name(self, name):
        self._name = name

    @flag.setter
    def flag(self, flag):
        self._flag = flag

    def __repr__(self):
        return f"{{'ip_address':{self._ip_address}, 'name':{self._name}, 'flag':{self._flag}}}"

    def __str__(self):
        return f'{self._ip_address:>15} - {self._name:6} - {"active" if self._flag else "disabled"}'

