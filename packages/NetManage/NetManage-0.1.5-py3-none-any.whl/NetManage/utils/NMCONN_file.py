from NetManage.utils.connections import COM_CONNECTION, SSH_CONNECTION, TELNET_CONNECTION, TFTP_CONNECTION


def read_nmconn(file: str) -> COM_CONNECTION | SSH_CONNECTION | TELNET_CONNECTION | TFTP_CONNECTION:
    with open(file, 'r') as f:
        lines = f.readlines()
        conn_data = {}
        for idx, line in enumerate(lines):
            line = line.strip()
            if len(line) > 0 and line[0:2] != '--':
                key, value = line.split(': ')
                print(key, value)
                conn_data[key] = value
        print(conn_data)

        if conn_data.get("DEVICE") is None:
            raise ValueError("DEVICE is not defined")

        if conn_data.get("METHOD") == "COM":
            print(conn_data.get("PORT"), conn_data.get("PORT") is None)
            print(conn_data.get("BAUDRATE"), conn_data.get("BAUDRATE") is None)
            if conn_data.get("PORT") is None or conn_data.get("BAUDRATE") is None:
                raise AttributeError("Expected more data.")
            return COM_CONNECTION(conn_data)
        elif conn_data.get("METHOD") == "SSH":
            print(conn_data.get("HOST"), conn_data.get("HOST") is None)
            print(conn_data.get("PORT"), conn_data.get("PORT") is None)
            print(conn_data.get("USERNAME"), conn_data.get("USERNAME") is None)
            print(conn_data.get("PASSWORD"), conn_data.get("PASSWORD") is None)

            if conn_data.get("HOST") is None or conn_data.get("PORT") is None or conn_data.get("USERNAME") is None or conn_data.get("PASSWORD") is None:
                raise AttributeError("Expected more data.")
            return SSH_CONNECTION(conn_data)

        elif conn_data.get("METHOD") == "TELNET":
            print(conn_data.get("HOST"), conn_data.get("HOST") is None)
            print(conn_data.get("PORT"), conn_data.get("PORT") is None)
            print(conn_data.get("PASSWORD"), conn_data.get("PASSWORD") is None)

            if conn_data.get("HOST") is None or conn_data.get("PORT") is None or conn_data.get("PASSWORD") is None:
                raise AttributeError("Expected more data.")
            return TELNET_CONNECTION(conn_data)

        elif conn_data.get("METHOD") == "TFTP":
            return TFTP_CONNECTION()
        else:
            raise AttributeError("Unknown or unhandled connection type.")

def create_nmconn(name, output, method, device, ip, port, username, password, exec, baudrate):
    if output is not None:
        with open(output, 'w+', encoding="UTF-8") as f:
            f.writelines([
                "-- META\n",
                f"NAME: {name}\n",
                f"METHOD: {method}\n",
            ])

            if method == "COM":
                f.writelines([
                    "-- DATA\n",
                    f"PORT: {port}\n",
                    f"BAUDRATE: {baudrate}\n",
                    f"EXECPASS: {exec}\n",
                ])
            elif method == "SSH":
                f.writelines([
                    "-- DATA\n",
                    f"HOST: {ip}\n",
                    f"PORT: {port}\n",
                    f"USERNAME: {username}\n",
                    f"PASSWORD: {password}\n",
                    f"EXECPASS: {exec}\n",
                ])
            elif method == "TELNET":
                f.writelines([
                    "-- DATA\n",
                    f"HOST: {ip}\n",
                    f"PORT: {port}\n",
                    f"PASSWORD: {password}\n",
                    f"EXECPASS: {exec}\n",
                ])
            f.writelines([
                "-- DEVICE\n",
                f"DEVICE: {device}\n"
            ])