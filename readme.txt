sudo apt install zmap
man zmap
sudo zmap -B 10M -p 80 -o result.csv -t 14400 -b blacklist.txt -r 300
# use -B to limit the bandwidth, so you do not cause internet traffic.
# use -r to set send rate in packets/sec, to avoid too fast and lose packets.
# use -t to cap the length of time for sending packets. 14400 = 4 hours

zmap --version
zmap --list-output-fields
sudo zmap -p 80 -o zmapscan0818.csv -t 14400 -b blacklist.txt -r 300 -f "saddr,daddr,ipid,ttl,sport,dport,seqnum,acknum,window,classification,success,repeat,cooldown,timestamp-str"

# ---------------------------------------------------------------------------- #
Network		NIP	Example IP	Owner
104.16.0.0/12	154	104.17.80.50	Cloudflare, Inc.

sudo zmap 104.16.0.0/12 -p 22 -o cloudflare_p22.csv -b blacklist.txt -t 60 -r 300 -f "saddr,daddr,ipid,ttl,sport,dport,seqnum,acknum,window,classification,success,repeat,cooldown,timestamp-str"

sudo zmap 104.16.0.0/12 -p 443 -o cloudflare_p443.csv -b blacklist.txt -t 60 -r 300 -f "saddr,daddr,ipid,ttl,sport,dport,seqnum,acknum,window,classification,success,repeat,cooldown,timestamp-str"

# port 20, FTP
# port 22, SSH
# port 25, SMTP
# port 80, HTTP
# port 443, HTTPS

# ---------------------------------------------------------------------------- #

censys.io

sudo tcpdump -i any -w ff_cat0.pcap

sudo apt install openconnect
sudo openconnect vpn.utexas.edu

https://stackoverflow.com/questions/15316304/open-tor-browser-with-selenium

https://github.com/webfp/tor-browser-selenium/issues/116

https://kushaldas.in/posts/tor-browser-and-selenium.html

# ---------------------------------------------------------------------------- #
sudo zmap -B 10M -p 80 -o zmapscan.txt -t 14400 -b blacklist.txt -r 300
After 4 hours, got 16204 IP addresses

Stephan said using AWS c5.12xlarge instance, he got 580875 in 15 minutes...
TODO give it a try

# ---------------------------------------------------------------------------- #
python
import ipaddress

ipaddress.ip_network('8.8.8.0/24')

net = ipaddress.ip_network('8.8.8.0/24')
new_ip = ipaddress.IPv4Address('8.8.8.9')
new_ip in net

new_ip = ipaddress.IPv4Address('9.8.8.9')
new_ip in net

# ---------------------------------------------------------------------------- #

Get command line output within python
python3 subprocess
python2 commands
import subprocess
s,o = subprocess.getstatusoutput("ls")
s,o = subprocess.getstatusoutput("tshark -r /tmp/tst.pcap")

# ---------------------------------------------------------------------------- #

Wireshark filter source 
ip.src == 10.0.2.15 or ip.dst == 10.0.2.15

# ---------------------------------------------------------------------------- #
How To: Find IP Address Owner
https://www.cyberciti.biz/faq/find-ip-address-owner/
$ host 
$ whois

Find IP Address For A Host Name

$ host github.com
www.github.com is an alias for github.com.
github.com has address 140.82.113.4

$ nslookup github.com
Server:		127.0.0.53
Address:	127.0.0.53#53
Non-authoritative answer:
Name:	github.com
Address: 140.82.113.4
# ---------------------------------------------------------------------------- #
whois - client for the whois directory service
whois searches for an object in a RFC 3912 database.

$ whois github.com
$ whois 140.82.113.4

Use the IP address to get the NetRange and CIDR
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
