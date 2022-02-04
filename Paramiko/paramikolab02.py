import os
import time
import paramiko

username = 'admin'
devices_ip = ["172.31.107.4", "172.31.107.5", "172.31.107.6"]

for ip in devices_ip:
    client = paramiko.SSHClient()
    with open("paramiko_privateKey", 'r') as file:
        privateKey = paramiko.RSAKey.from_private_key(file)

        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=username, allow_agent=False, pkey=privateKey, look_for_keys=True)
        print("Connecting to {} ...".format(ip))
        with client.invoke_shell() as ssh:
            print("Connected to {} ...".format(ip))

            ssh.send("terminal length 0\n")
            time.sleep(1)
            result = ssh.recv(1000).decode('ascii')
            print(result)
