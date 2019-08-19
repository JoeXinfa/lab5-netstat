#import pandas as pd
from openweb import sites
from collections import OrderedDict as odict

def main():
    packets = load_pcap_files()
    print(len(packets))
    for k,v in packets.items():
        print(k)


def read_pcap_file(fn):
    #df = pd.read_csv(fn, sep='\s+', header=None, skipinitialspace=True)
    packets = []
    with open(fn, 'r') as f:
        for line in f:
            line = line.strip('\n')
            cols = line.split()
            seq = cols[0]
            sip = cols[2]
            dip = cols[4]
            prot = cols[5]
            plen = cols[6]
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
                pkt = read_pcap_file(fn)
                key = "{}_{}_{}".format(mode, site, i)
                packets[key] = pkt
    return packets


if __name__ == '__main__':
    main()
