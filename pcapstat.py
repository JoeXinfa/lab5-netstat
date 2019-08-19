import pandas as pd
from openweb import sites
from collections import OrderedDict as odict


def main():
    packets = load_pcap_files()
    print(len(packets))

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
                fn = "{}_{}_{}.pcap.txt".format(path, site, i)
                #print(fn)
                pkt = read_pcap_csv(fn)
                key = "{}_{}_{}".format(mode, site, i)
                packets[key] = pkt
    return packets


if __name__ == '__main__':
    main()
