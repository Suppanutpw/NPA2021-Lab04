#pylint: disable=invalid-name
#pylint: disable=missing-module-docstring
import pexpect

PROMPT = '#'
BASHIONIP = '10.0.15.107'
ADDRESSES = [
    ['172.31.107.4', '1.1.1.1'], 
    ['172.31.107.5', '2.2.2.2'],
    ['172.31.107.6', '3.3.3.3']
]
USERNAME = 'admin'
PASSWORD = 'cisco'
COMMAND = 'sh ip int bri'

child = pexpect.spawn('telnet ' + BASHIONIP)
child.expect('Username')
child.sendline(USERNAME)
child.expect('Password')
child.sendline(PASSWORD)
child.expect(PROMPT)

for address, loopback in ADDRESSES:
    child.sendline('telnet ' + address)
    child.expect('Username')
    child.sendline(USERNAME)
    child.expect('Password')
    child.sendline(PASSWORD)
    child.expect(PROMPT)
    child.sendline('conf t')
    child.expect(PROMPT)
    child.sendline('int loopback 0')
    child.expect(PROMPT)
    child.sendline('ip address ' + loopback + ' 255.255.255.255')
    child.expect(PROMPT)
    child.sendline('exit') # interface config
    child.expect(PROMPT)
    child.sendline('exit') # config
    child.expect(PROMPT)
    child.sendline('write')
    child.expect(PROMPT)
    child.sendline('exit') # privilege
    child.expect(PROMPT)
