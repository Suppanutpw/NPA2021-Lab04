import time
import paramiko

username = 'admin'
devices_ip = ["172.31.107.4", "172.31.107.5", "172.31.107.6"]

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=username, key_filename="paramiko_privateKey", look_for_keys=True)
    print("Connecting to {} ...".format(ip))
    with client.invoke_shell() as ssh:
        print("Connected to {} ...".format(ip))

        ssh.send("terminal length 0\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)

        ssh.send("sh ip int br\n")
        time.sleep(1)
        result = ssh.recv(1000).decode('ascii')
        print(result)