import subprocess
import netaddr
#import ipaddress
import os
from joblib import Parallel, delayed
import sys
import pickle

KEYS = ('NetRange', 'CIDR', 'inetnum')


def get_subnet_from_whois(ip):
    """
    $ whois 23.56.58.59 returns two CIDR
      CIDR:           23.56.32.0/19
      CIDR:           23.32.0.0/11, 23.64.0.0/14
    """
    subs = {'CIDR': None, 'NetRange': None, 'inetnum': None}
    try:
        s,o = subprocess.getstatusoutput("whois {}".format(ip))
    except UnicodeDecodeError:
        return None
    out = o.split('\n')
    for line in out:
        if len(line) == 0 or line[0] in ('#', '%'):
            continue
        if any(key in line for key in KEYS):
            k, v = line.split(':')[:2]
            if k not in KEYS: # netname: GCTR-CIDR-BLK-JP
                continue
            v = v.strip()
            #val = val.split(',')[0] # for some cases
            if subs[k] is None: # only take the first appearance
                subs[k] = v
    if all(subs[key] is None for key in KEYS):
       return None
       #raise ValueError("No subnet found from whois")
    return subs


def cidr2range(cidr):
    """
    NetRange:   23.192.0.0 - 23.223.255.255
    CIDR:       23.192.0.0/11
    """
    c = netaddr.IPNetwork(cidr)
    startip = c.ip # object netaddr.IPAddress
    endip = c.broadcast # object netaddr.IPAddress
    return str(startip) + ' - ' + str(endip)


def range2cidr(netrange):
    """
    NetRange:   23.192.0.0 - 23.223.255.255
    CIDR:       23.192.0.0/11
    """
    startip, endip = netrange.split('-')
    cidr = netaddr.iprange_to_cidrs(startip, endip)[0]
    # cidr is object netaddr.IPNetwork('23.192.0.0/11')
    return str(cidr)


def complete_subnet(subs):
    """
    Some return of 'whois ip' have inetnum, no CIDR or NetRange.
    Some inetnum is in range, some in prefix.
    This function ensures CIDR and NetRange are ready.
    """
    if subs['NetRange'] is not None:
        if subs['CIDR'] is not None: # consistency check
            if subs['CIDR'] != range2cidr(subs['NetRange']):
                #raise ValueError("CIDR calculated {} != CIDR whois {}".format(
                #    range2cidr(subs['NetRange']), subs['CIDR']))
                subs = None # flag as bad IP
            if subs['NetRange'] != cidr2range(subs['CIDR']):
                #raise ValueError("NetR calculated {} != NetR whois {}".format(
                #    cidr2range(subs['CIDR']), subs['NetRange']))
                subs = None # flag as bad IP
        else:
            subs['CIDR'] = range2cidr(subs['NetRange'])
    else:
        if subs['CIDR'] is not None:
            subs['NetRange'] = cidr2range(subs['CIDR'])
        else: # calculate from inetnum
            if '-' in subs['inetnum']:
                subs['NetRange'] = subs['inetnum']
                subs['CIDR'] = range2cidr(subs['NetRange'])
            elif '/' in subs['inetnum']:
                subs['CIDR'] = subs['inetnum']
                subs['NetRange'] = cidr2range(subs['CIDR'])
            else:
                raise ValueError("inetnum in wrong format")
    return subs


def find_subnet(i, ip):
    if i % 10 == 0:
        print('working on {} {}'.format(i, ip))
    subs = get_subnet_from_whois(ip)
    if subs is None:
        return (ip, None)
    if subs['CIDR'] is not None:
        if ',' in subs['CIDR']:
            return (ip, None)
    subs = complete_subnet(subs)
    return (ip, subs)


def main():
    fn = sys.argv[1]
    #fn = "zmapscan.txt"
    ips = []
    with open(fn, 'r') as f:
        for ip in f:
            ip = ip.strip('\n')
            ips.append(ip)

    #nthread = os.cpu_count()
    nthread = 100 # this can be bigger than cores, why?
    nip = len(ips)
    lista = Parallel(n_jobs=nthread)(delayed(find_subnet)(i, ips[i])
        for i in range(nip))

    badips = []
    subnets = {}
    for ipnet in lista:
        ip, net = ipnet
        if net is None:
            badips.append(ip)
            continue
        cidr = net['CIDR']
        if cidr not in subnets:
            subnets[cidr] = [ip]
        else:
            subnets[cidr].append(ip)

    nipfit = 0
    for key,val in subnets.items():
        nipfit += len(val)

    print('Number of networks =', len(subnets))
    print('Number of IPs in output =', nipfit)
    print('Number of IPs in input =', nip)
    print('Number of bad IPs =', len(badips))

    outfn = 'subnets.pkl'
    pickle.dump(subnets, open(outfn, 'wb'))
    #test = pickle.load(open(outfn, 'rb'))
    #print(test)

    outfn = 'badips.pkl'
    pickle.dump(badips, open(outfn, 'wb'))


if __name__ == '__main__':
    main()
