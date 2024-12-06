class COM_CONNECTION:
    def __init__(self, data: dict):
        self.NAME = data["NAME"]
        self.METHOD = "COM"
        self.PORT = data["PORT"]
        self.BAUDRATE = data["BAUDRATE"]
        self.DEVICE = data["DEVICE"]+"_serial"
        self.EXECPASS = data["EXECPASS"] if data.get("EXECPASS") else ""

    def __str__(self):
        return f"{self.METHOD}, {self.PORT}, {self.BAUDRATE}, {self.DEVICE}, {self.EXECPASS}"

    def getNetmikoConnDict(self):
        return {
            'device_type': self.DEVICE,
            'serial_settings': {
                'port': self.PORT,
                'baudrate': self.BAUDRATE,
            },
            'username': '',
            'password': '',
            'secret': self.EXECPASS,
        }

class SSH_CONNECTION:
    def __init__(self, data: dict):
        self.NAME = data["NAME"]
        self.METHOD = data["METHOD"]
        self.HOST = data["HOST"]
        self.PORT = data["PORT"]
        self.USERNAME = data["USERNAME"]
        self.PASSWORD = data["PASSWORD"]
        self.DEVICE = data["DEVICE"]
        self.EXECPASS = data["EXECPASS"] if data.get("EXECPASS") else ""

    def __str__(self):
        return f"{self.METHOD}, {self.HOST}, {self.PORT}, {self.USERNAME}, {self.PASSWORD}, {self.EXECPASS}"

    def getNetmikoConnDict(self):
        return {
            'device_type': self.DEVICE,
            'host': self.HOST,
            'port': self.PORT,
            'username': self.USERNAME,
            'password': self.PASSWORD,
            'secret': self.EXECPASS,
        }

class TELNET_CONNECTION:
    def __init__(self, data: dict):
        self.NAME = data["NAME"]
        self.METHOD = data["METHOD"]
        self.HOST = data["HOST"]
        self.PORT = data["PORT"]
        self.PASSWORD = data["PASSWORD"]
        self.DEVICE = data["DEVICE"] + "_telnet"
        self.EXECPASS = data["EXECPASS"] if data.get("EXECPASS") else ""

    def __str__(self):
        return f"{self.METHOD}, {self.HOST}, {self.PORT}, {self.PASSWORD}, {self.EXECPASS}"

    def getNetmikoConnDict(self):
        return {
            'device_type': self.DEVICE,
            'host': self.HOST,
            'port': self.PORT,
            'password': self.PASSWORD,
            'secret': self.EXECPASS,
        }

class TFTP_CONNECTION:
    pass