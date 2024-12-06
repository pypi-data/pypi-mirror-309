class INPUT:
    type = None
    id = None
    label = None

    def read(self, line: str):
        line = line.strip().split(";")
        self.type, self.id, self.label = line[0], line[1], line[2]

    def toTuple(self):
        return self.type, self.id, self.label

    def __str__(self):
        return f"{self.type};{self.id};{self.label}"

class COMMAND:
    def __init__(self, meta_section: dict, commands_section: list[str], devices_section: list[str], inputs_section: list[INPUT]):
        self.NAME = meta_section["NAME"]
        self.TYPE = meta_section["TYPE"]
        self.commands = commands_section
        self.devices = devices_section
        self.inputs_section = inputs_section

    def __str__(self):
        return f"{self.NAME} {self.TYPE} {self.commands} {self.devices} {self.inputs_section}"

