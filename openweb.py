# needed for Tor
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# needed for other
from selenium import webdriver

import sys
#import time
import subprocess as sub

n = 10
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

def main():
    mode = sys.argv[1]
    
    if mode == 'tor':
        # this is wherever your firefox script that Tor installs is
        binary = '/home/joseph/Downloads/tor-browser-linux64-8.5.4_en-US/tor-browser_en-US/Browser/firefox'
        firefox_binary = FirefoxBinary(binary)
        #browser = webdriver.Firefox(firefox_binary=firefox_binary)
    elif mode == 'firefox':
        # this is wherever your geckodriver you downloaded is
        binary= '/usr/local/bin'
        #browser = webdriver.Firefox(binary)
    else:
        raise NotImplementedError
    
    #from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    #cap = DesiredCapabilities().FIREFOX.copy()
    #cap['marionette'] = False
    
    for i in range(n):
        for site in sites:
            short, url = site
            print("------ work {} {}".format(i, url))
            # Open a new browser for each pcap
            if mode == 'tor':
                browser = webdriver.Firefox(firefox_binary=firefox_binary)
                #browser = webdriver.Firefox(firefox_binary=firefox_binary, capabilities=cap)
            if mode == 'firefox':
                browser = webdriver.Firefox(binary)
            fn = "{}_{}_{}.pcap".format(mode, short, i)
            sub.Popen(['sudo', 'tcpdump', '-i', 'any', '-w', fn])
            browser.get(url)
            browser.quit()
            sub.Popen(['sudo', 'killall', 'tcpdump'])


if __name__ == '__main__':
    main()
