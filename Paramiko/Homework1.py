import time
import paramiko

username = 'admin'
password = 'cisco'

devices_ip = ["172.31.107.4", "172.31.107.5", "172.31.107.6"]

class RouterConfig:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect (hostname=ip, username=username, password=password, look_for_keys=False)
        self.commands = ["terminal length 0", "conf t"] # start from config mode
        print("Connecting to {}...".format(ip))

    def run(self):
        self.commands.append("exit") # config -> privilege
        self.commands.append("write") # save config
        self.commands.append("exit") # closed connection
        with self.client.invoke_shell() as ssh:
            print("Connected to {}".format(self.ip))
            for command in self.commands:
                ssh.send(command + "\n")
                time.sleep(0.3)
                result = ssh.recv(5000).decode('ascii')
                print (result, end="")

    def DHCPClient(self, interface):
        self.commands.append("int " + interface)
        self.commands.append("vrf forwarding control-Data")
        self.commands.append("ip address dhcp")
        self.commands.append("no shutdown")
        self.commands.append("exit") # interface config -> config

    def StaticIP(self, interface, address, subnet):
        self.commands.append("int " + interface)
        self.commands.append("vrf forwarding control-Data")
        self.commands.append("ip address %s %s"%(address, subnet))
        self.commands.append("no shutdown")
        self.commands.append("exit") # interface config -> config

    def addOSPFNetwork(self, address, wildcard):
        self.commands.append("router ospf 1 vrf control-Data")
        self.commands.append("network %s %s area 0"%(address, wildcard))
        self.commands.append("exit") # router ospf -> config

    def redistributeOSPF(self):
        self.commands.append("router ospf 1")
        self.commands.append("default-information originate")
        self.commands.append("exit") # router ospf -> config

    def setNATInterface(self, interface, side):
        self.commands.append("int " + interface)
        self.commands.append("ip nat " + side)
        self.commands.append("exit")
    
    def PAT(self, address, wildcard, listNum, interface):
        self.commands.append("access-list %d permit %s %s"%(listNum, address, wildcard))
        self.commands.append("ip nat inside source list %d interface %s vrf control-Data overload"%(listNum, interface))

    def setVTYACL(self, listName, permitIPs):
        self.commands.append("ip access-list standard " + listName)
        for i in range(len(permitIPs)):
            self.commands.append("%d permit %s %s"%(((i+1)*10), permitIPs[i][0], permitIPs[i][1]))
        self.commands.append("exit") # config-std-nacl -> config
        self.commands.append("line vty 0 4")
        self.commands.append("access-class %s in"%listName)
        self.commands.append("exit") # line-vty -> config

R1 = RouterConfig(devices_ip[0], username, password)
R1.StaticIP('g0/1', '172.31.107.17', '255.255.255.240')
R1.StaticIP('g0/2', '172.31.107.33', '255.255.255.240')
R1.addOSPFNetwork('172.31.107.16', '0.0.0.15')
R1.addOSPFNetwork('172.31.107.32', '0.0.0.15')
R1.setVTYACL('allowManageandVPN', [('172.31.107.0', '0.0.0.15'), ('10.253.190.0', '0.0.0.255')])

R2 = RouterConfig(devices_ip[1], username, password)
R2.StaticIP('g0/1', '172.31.107.34', '255.255.255.240')
R2.StaticIP('g0/2', '172.31.107.49', '255.255.255.240')
R2.addOSPFNetwork('172.31.107.32', '0.0.0.15')
R2.addOSPFNetwork('172.31.107.48', '0.0.0.15')
R2.setVTYACL('allowManageandVPN', [('172.31.107.0', '0.0.0.15'), ('10.253.190.0', '0.0.0.255')])

R3 = RouterConfig(devices_ip[2], username, password)
R3.DHCPClient('g0/2')
R3.StaticIP('g0/1', '172.31.107.50', '255.255.255.240')
R3.addOSPFNetwork('172.31.107.48', '0.0.0.15')
R3.redistributeOSPF()
R3.setNATInterface('g0/1', 'inside')
R3.setNATInterface('g0/2', 'outside')
R3.PAT('172.31.107.0', '0.0.0.255', 7, 'g0/2')
R3.setVTYACL('allowManageandVPN', [('172.31.107.0', '0.0.0.15'), ('10.253.190.0', '0.0.0.255')])

R1.run()
R2.run()
R3.run()
