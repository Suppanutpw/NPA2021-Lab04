import time
from jinja2 import Template
import json
import paramiko

jsonFile = open("Routers.json", "r")
routersJson = json.load(jsonFile)
jsonFile.close()

templateFile = open("template.j2", "r").read()
template = Template(templateFile)

for routerJson in routersJson:
    print(routerJson['Interfaces'])
    commands = template.render(
        interfaces = routerJson['Interfaces'],
        ospf = routerJson['OSPF'],
        vtyacl = routerJson['VTYACL'],
        pat = routerJson.get('PAT', None)
    )

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect (hostname=routerJson['IP'], username=routerJson['Username'], password=routerJson['Password'], look_for_keys=False)
    print("Connecting to {}...".format(routerJson['IP']))

    commands = commands.splitlines()
    with client.invoke_shell() as ssh:
        print("Connected to {}".format(routerJson['IP']))
        for command in commands:
            command = command.strip()
            if (command):
                ssh.send(command + "\n")
                time.sleep(0.1)
                result = ssh.recv(5000).decode('ascii')
                print(result, end="")

