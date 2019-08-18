import subprocess as sub
import netaddr

KEYS = ('NetRange', 'CIDR', 'inetnum')


def get_subnet_from_whois(ip):
    """
    $ whois 23.56.58.59 returns two CIDR
      CIDR:           23.56.32.0/19
      CIDR:           23.32.0.0/11, 23.64.0.0/14
    """
    subs = {'CIDR': None, 'NetRange': None, 'inetnum': None}
    s,o = sub.getstatusoutput("whois {}".format(ip))
    out = o.split('\n')
    for line in out:
        if len(line) == 0 or line[0] in ('#', '%'):
            continue
        if any(key in line for key in KEYS):
            key, val = line.split(':')
            val = val.strip()
            #val = val.split(',')[0] # for some cases
            if subs[key] is None: # only take the first appearance
                subs[key] = val
    if all(subs[key] is None for key in KEYS):
       raise ValueError("No subnet found from whois")
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
                raise ValueError("CIDR calculated != CIDR whois")
            if subs['NetRange'] != cidr2range(subs['CIDR']):
                raise ValueError("NetR calculated != NetR whois")
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


def main():
    #fn = "zmapscan.txt"
    fn = "test.txt"
    with open(fn, 'r') as f:
        for ip in f:
            ip = ip.strip('\n')
            subs = get_subnet_from_whois(ip)
            complete_subnet(subs)
            print("{} \t {}".format(ip, subs))


if __name__ == '__main__':
    main()
