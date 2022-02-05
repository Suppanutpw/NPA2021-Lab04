import getpass
import telnetlib
import time

host = "10.0.15.107"
user = input("Ebter username: ")
password = getpass.getpass()

tn = telnetlib.Telnet(host, 23, 5)

# Telnet เข้าไปยัง R0
tn.read_until(b"Username:")
tn.write(user.encode('ascii') + b"\n")
time.sleep(1)

tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n")
time.sleep(1)

# ใช้ R0 telnet ไปยัง R1 เพื่อ config
tn.write(b"telnet 172.31.107.4\n")
tn.read_until(b"Username:")

tn.write(user.encode('ascii') + b"\n")
time.sleep(1)

tn.read_until(b"Password:")
tn.write(password.encode('ascii') + b"\n")
time.sleep(1)

tn.write(b"conf t\n")
tn.write(b"int g0/1\n")
tn.write(b"ip add 172.31.107.17 255.255.255.240\n")
tn.write(b"no shut\n")
tn.write(b"exit\n")
tn.write(b"exit\n")
tn.write(b"wr\n")
time.sleep(2)
tn.write(b"show ip int br\n")
time.sleep(2)

output = tn.read_very_eager()
print(output.decode('ascii'))

tn.close