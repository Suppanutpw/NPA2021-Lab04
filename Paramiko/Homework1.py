import time
import paramiko

username = 'admin'
password = 'cisco'

devices_ip = ["172.31.107.4", "172.31.107.5", "172.31.107.6"]

class config:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect (hostname=ip, username=username, password=password, look_for_keys=False)
        self.commands = [] # start from privilege mode
        print("Connecting to {}...".format(ip))

    def run():
        with self.client.invoke_shell() as ssh:
            print("Connected to {}".format(self.ip))
            for command in commands:
                ssh.send("terminal length 0\n")
                time.sleep(2)
                result = ssh.recv(5000).decode('ascii')
                print (result)


    def DHCPClient(interface):
        self.commands.append("conf t") # privilege -> config
        self.commands.append("int " + interface)
        self.commands.append("ip address dhcp")
        self.commands.append("exit") # interface config -> config
        self.commands.append("exit") # config -> privilege

    def StaticIP(address, subnet):
        self.commands.append("conf t") # privilege -> config
        self.commands.append("int " + interface)
        self.commands.append("vrf forwarding control-Data")
        self.commands.append("ip address " + address + " " + subnet)
        self.commands.append("exit") # interface config -> config
        self.commands.append("exit") # config -> privilege

    def addOSPFNetwork(address, netmask):
        self.commands.append("conf t") # privilege -> config
        self.commands.append("router ospf 1")
        self.commands.append("network " + address + " " + netmask)
        self.commands.append("exit") # router ospf -> config
        self.commands.append("exit") # config -> privilege

    def redistributeOSPF():
        self.commands.append("conf t") # privilege -> config
        self.commands.append("router ospf 1")
        self.commands.append("redistribute static")
        self.commands.append("exit") # router ospf -> config
        self.commands.append("exit") # config -> privilege

    def PAT():
        pass

    def ACL():
        pass

R1 = config(devices_ip[0], username, password)
