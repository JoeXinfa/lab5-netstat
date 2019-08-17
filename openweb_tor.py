import sys
import time
import subprocess as sub
from tbselenium.tbdriver import TorBrowserDriver

# Point the path to the tor-browser_en-US directory in your system
tbpath = '/home/joseph/Downloads/tor-browser-linux64-8.5.4_en-US/tor-browser_en-US/'
driver = TorBrowserDriver(tbpath, tbb_logfile_path='test.log')

n = 1
sites = [
    ('cat', "https://en.wikipedia.org/wiki/Cat"),
    ('dog', "https://en.wikipedia.org/wiki/Dog"),
    ('egr', "https://en.wikipedia.org/wiki/Egress_filtering"),
    ('mit', "http://web.mit.edu/"),
    ('unm', "http://www.unm.edu/"),
    ('cmu', "https://www.cmu.edu/"),
    ('bkl', "https://www.berkeley.edu/"),
    ('utx', "https://www.utexas.edu/"),
    ('asu', "https://www.asu.edu/"),
    ('utd', "https://www.utdallas.edu/")]

sites = [
    ('cat', "https://en.wikipedia.org/wiki/Cat")]

for i in range(n):
    for site in sites:
        short, url = site
        print("------ work {} {}".format(i, url))
        #browser = webdriver.Firefox(binary)
        fn = "{}_{}_{}.pcap".format(mode, short, i)
        sub.Popen(['sudo', 'tcpdump', '-i', 'any', '-w', fn])
        driver.load_url(url)
        driver.close()
        sub.Popen(['sudo', 'killall', 'tcpdump'])
