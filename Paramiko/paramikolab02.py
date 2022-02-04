import time
import paramiko

username = 'admin'
# password = 'cisco'

# devices_ip = ["172.31.107.4", "172.31.107.5", "172.31.107.6"]
devices_ip = ["172.31.107.4"]

for ip in devices_ip:
    client = paramiko.SSHClient()
    client.load_system_host_keys("paramiko_privateKey.ppk")
    privateKey = client.get_host_keys()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, username=username, pkey=privateKey, look_for_keys=True)
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