# needed for Tor
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# needed for other
from selenium import webdriver

import sys
import time
import subprocess as sub

mode = sys.argv[1]

if (mode == 'tor'):
    # this is wherever your firefox script that Tor installs is
    binary = '/home/seed/Downloads/tor-browser_en-US/Browser/firefox'
    firefox_binary = FirefoxBinary(binary)
    browser = webdriver.Firefox(firefox_binary=binary)
elif (mode == 'firefox'):
    # this is wherever your geckodriver you downloaded is
    binary= '/usr/local/bin'
    browser = webdriver.Firefox(binary)
else:
    raise NotImplementedError

# tcpdump call goes here

urls = [
    "https://en.wikipedia.org/wiki/Cat",
    "https://en.wikipedia.org/wiki/Dog",
    "https://en.wikipedia.org/wiki/Egress_filtering",
    "http://web.mit.edu/",
    "http://www.unm.edu/",
    "https://www.cmu.edu/",
    "https://www.berkeley.edu/",
    "https://www.utexas.edu/",
    "https://www.asu.edu/",
    "https://www.utdallas.edu/"]

urls = ["https://en.wikipedia.org/wiki/Cat"]
fns = ["cat", "dog", "egr", "mit", "unm", "cmu", "bkl", "utx", "asu", "utd"]
tmp = 'tmp.pcap'

for i in range(0):
  for url in urls: # or whatever
    print("work {}".format(url))
    fn = "{}_{}_{}.pcap".format(mode, fns[urls.index(url)], i)
    s,o = sub.getstatusoutput("rm -f {}".format(tmp))
    #pro = sub.Popen(['tcpdump', '-i', 'any', '-w', fn],
    pro = sub.Popen(['sudo', 'tcpdump', '-i', 'any', '-w', tmp],
        stdout=sub.PIPE, stderr=sub.STDOUT)
    browser.get(url)
    time.sleep(5)
    # Need to stop dump to the pcap file
    #pro.kill()
    s,o = sub.getstatusoutput("cp {} {}".format(tmp, fn))
    print("done {}".format(url))
