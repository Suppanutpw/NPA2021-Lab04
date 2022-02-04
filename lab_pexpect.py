#pylint: disable=invalid-name
#pylint: disable=missing-module-docstring
import pexpect

PROMPT = '#'
IP = '10.0.15.107'
USERNAME = 'admin'
PASSWORD = 'cisco'
COMMAND = 'sh ip int bri'

child = pexpect.spawn('telnet ' + IP)
child.expect('Username')
child.sendline(USERNAME)
child.expect('Password')
child.sendline(PASSWORD)
child.expect(PROMPT)
child.sendline(COMMAND)
child.expect(PROMPT)
result = child.before
print(result.decode('UTF-8'))
child.sendline('exit')
