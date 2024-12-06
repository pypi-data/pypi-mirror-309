from NetManage.utils.commands import COMMAND, INPUT


def read_NMCOMM(file:str) -> COMMAND:
    meta_section = {}
    commands_section = []
    devices_section = []
    inputs_section = []

    with open(file, 'r') as f:
        lines = f.readlines()
        curr_section = None
        for idx, line in enumerate(lines):
            line = line.strip()
            print(line)
            if line == "-- META":
                print("META")
                curr_section = meta_section
            elif line == "-- COMMANDS":
                print("COMMAND")
                curr_section = commands_section
            elif line == "-- DEVICES":
                print("DEVICES")
                curr_section = devices_section
            elif line == "-- INPUTS":
                print("INPUTS")
                curr_section = inputs_section

            if line[0:2] == '--':
                continue

            if curr_section is meta_section:
                if len(line) > 0:
                    key, value = line.split(': ')
                    print(key, value)
                    curr_section[key] = value

            if curr_section is commands_section or curr_section is devices_section:
                curr_section.append(line)

            if curr_section is inputs_section:
                new_input = INPUT()
                new_input.read(line)
                curr_section.append(new_input)


    if not validate_NMCOM_file(meta_section, commands_section, devices_section, inputs_section):
        raise Exception("Invalid NMCOM file")

    command = COMMAND(meta_section, commands_section, devices_section, inputs_section)
    print(inputs_section[0])
    return command

def validate_NMCOM_file(meta_section, commands_section, devices_section, inputs_section):
    meta_keys = meta_section.keys()

    if not (len(meta_keys) == 2 and "NAME" in meta_keys and "TYPE" in meta_keys):
        return False
    if len(commands_section) == 0:
        return False
    if len(devices_section) == 0:
        return False
    return True



if __name__ == '__main__':
    read_NMCOMM("../commands/set_hostname.nmcomm")