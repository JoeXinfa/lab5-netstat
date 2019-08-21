import pandas as pd
from openweb import sites
from collections import OrderedDict as odict
import matplotlib.pyplot as plt
import numpy as np

MYIP = '10.0.2.15'

"""
SRIP = {'firefox_cat': ('10.0.2.15', '208.80.153.224'),
        'firefox_dog': ('10.0.2.15', '208.80.153.224'),
        'firefox_egr': ('10.0.2.15', '208.80.153.224'),
        'firefox_mit': ('10.0.2.15', '23.207.38.174'),
        'firefox_unm': ('10.0.2.15', '129.24.172.124'),
        'firefox_cmu': ('10.0.2.15', '128.2.42.52'),
        'firefox_bkl': ('10.0.2.15', '52.88.114.129'),
        'firefox_utx': ('10.0.2.15', '104.20.83.19'),
        'firefox_asu': ('10.0.2.15', '104.16.50.14'),
        'firefox_utd': ('10.0.2.15', '104.16.44.54'),
        'tor_cat': ('10.0.2.15', '51.15.50.36'),
}
"""


def main():
    packets = load_pcap_files()
#    average_packet_size(packets, 'firefox', 'cat', 1)

    modes = ['firefox', 'tor', 'vpn']
    n = 10
    apss = [] # average packet size
    npsent = []
    nprecv = []
    i = 0
    for mode in modes:
        for s in sites:
            site, url = s
            aps = average_packet_size(packets, mode, site, n)
            nps = average_npacket_sent(packets, mode, site, n)
            npr = average_npacket_recv(packets, mode, site, n)
            apss.append(aps)
            npsent.append(nps)
            nprecv.append(npr)
            print("{}\t{}\t{}\t{}\t{}\t{}".format(i, mode, site, aps, nps, npr))
            i += 1

    plot_bar(apss, 'Average Packet Size (bytes)', 'aps.png', 3)
    plot_bar(npsent, 'Average Number of Packets Sent', 'npsent.png', 2)
    plot_bar(npsent, 'Average Number of Packets Received', 'nprecv.png', 1)


def plot_bar(dat, label, fn, i):
    obj = ('cat', 'dog', 'egr', 'mit', 'unm', 'cmu', 'bkl', 'utx', 'asu', 'utd',
           'cat', 'dog', 'egr', 'mit', 'unm', 'cmu', 'bkl', 'utx', 'asu', 'utd',
           'cat', 'dog', 'egr', 'mit', 'unm', 'cmu', 'bkl', 'utx', 'asu', 'utd')
    color = ('red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red', 'red',
             'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green',
             'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue')
    ypos = np.arange(len(obj))
    plt.figure(i, figsize=(6.4, 7.2))
    plt.barh(ypos, dat, color=color)
    plt.yticks(ypos, obj)
    plt.xlabel(label)
#    plt.show()
    plt.savefig(fn)
    
    
def plot_line(dat, ylabel, fn, i):
    plt.figure(i)
    plt.plot(dat, 'ro')
    plt.plot(dat, 'b-')
    plt.xlabel('Connection ID')
    plt.ylabel(ylabel)
    plt.grid()
#    plt.show()
    plt.savefig(fn)


def average_npacket_recv(packets, mode, site, n):
    """ Get average number of packets recv of n times visit to (mode,site) """
    asum = 0
    for i in range(n):
        key = "{}_{}_{}".format(mode, site, i)
        df = packets[key]
        df = df.loc[df['dip'] == MYIP]
        asum += df.shape[0]
    return int(asum / n)


def average_npacket_sent(packets, mode, site, n):
    """ Get average number of packets sent of n times visit to (mode,site) """
    asum = 0
    for i in range(n):
        key = "{}_{}_{}".format(mode, site, i)
        df = packets[key]
        df = df.loc[df['sip'] == MYIP]
        asum += df.shape[0]
    return int(asum / n)


def average_packet_size(packets, mode, site, n):
    """ Get average packet size of n times visit to (mode,site) """
    asum = 0
    for i in range(n):
        key = "{}_{}_{}".format(mode, site, i)
        df = packets[key]
        dfs = df.loc[df['sip'] == MYIP]
        dfd = df.loc[df['dip'] == MYIP]
        df_clean = pd.concat([dfs, dfd], ignore_index=True)
        asum += df_clean.len.mean()
    return int(asum / n)


def read_pcap_csv(fn):
    """ comma separated """
    names = ['seq', 'sip', 'dip', 'len', 'proto']
    df = pd.read_csv(fn, names=names)
    return df


def read_pcap_txt(fn):
    """ space delimited, tshark -r test.pcap > readable.txt """
    packets = []
    with open(fn, 'r') as f:
        for line in f:
            line = line.strip('\n')
            cols = line.split()
            seq = int(cols[0])
            sip = cols[2]
            dip = cols[4]
            prot = cols[5]
            plen = int(cols[6])
            packets.append([seq, sip, dip, prot, plen])
    return packets


def load_pcap_files():
    packets = odict()
    paths = [('firefox', 'firefox/firefox'),
             ('tor'    , 'tor/tor'        ),
             ('vpn'    , 'vpn/firefox'    )]
    for p in paths:
        mode, path = p
        for s in sites:
            site, url = s
            for i in range(10):
                fn = "{}_{}_{}.pcap.csv".format(path, site, i)
                #print(fn)
                pkt = read_pcap_csv(fn)
                key = "{}_{}_{}".format(mode, site, i)
                packets[key] = pkt
    return packets


if __name__ == '__main__':
    main()
