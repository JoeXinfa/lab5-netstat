import pickle
from collections import OrderedDict as odict
import subprocess


"""
Network		NIP	Example IP	Owner
104.64.0.0/10	684	104.78.92.154	Akamai Technologies, Inc.
23.192.0.0/11	406	23.212.206.132	Akamai Technologies, Inc.
23.0.0.0/12	193	23.2.134.147	Akamai Technologies, Inc.
104.16.0.0/12	154	104.17.80.50	Cloudflare, Inc.
23.72.0.0/13	122	23.75.11.119	Akamai Technologies, Inc.
184.24.0.0/13	113	184.26.248.69	Akamai Technologies, Inc.
52.0.0.0/11	101	52.6.25.191	Amazon Technologies Inc.
34.192.0.0/10	97	34.213.203.238	Amazon Technologies Inc.
39.96.0.0/13	66	39.105.130.108	Aliyun Computing Co., LTD
18.128.0.0/9	60	18.136.65.48	Amazon Technologies Inc.
184.84.0.0/14	48	184.84.110.45	Akamai Technologies, Inc.
13.224.0.0/14	47	13.227.47.22	Amazon Technologies Inc.
35.192.0.0/12	47	35.194.67.14	Google LLC
52.32.0.0/11	43	52.40.136.250	Amazon Technologies Inc.
112.124.0.0/14	41	112.127.114.74	Aliyun Computing Co., LTD
3.128.0.0/9	41	3.215.10.76	Amazon Technologies Inc.
223.4.0.0/14	40	223.6.171.180	Aliyun Computing Co., LTD
196.16.0.0/14	36	196.16.175.66	ORG-IA41-AFRINIC
13.32.0.0/12	34	13.33.177.55	Amazon Technologies Inc.
107.172.0.0/14	33	107.174.150.96	ColoCrossing
"""

def main():
    fn = 'subnets0817.pkl'
    net = pickle.load(open(fn, 'rb'))

    net = sorted(net.items(), key=lambda kv: len(kv[1]), reverse=True)
    net = odict(net)

    print("{}\t\t{}\t{}\t{}".format('Network', 'NIP', 'Example IP', 'Owner'))
    i = 0
    for key,val in net.items():
        ip = val[0]
        org = get_value_from_whois(ip, 'OrgName')
        if org is None:
           org = get_value_from_whois(ip, 'organisation')
        if org is None:
           org = get_value_from_whois(ip, 'descr')
        print("{}\t{}\t{}\t{}".format(key, len(val), ip, org))
        i += 1
        if i == 20:
            exit()


def get_value_from_whois(ip, key):
    val = None
    try:
        s,o = subprocess.getstatusoutput("whois {}".format(ip))
    except UnicodeDecodeError:
        return None
    out = o.split('\n')
    for line in out:
        if val is not None:
            break
        if len(line) == 0 or line[0] in ('#', '%'):
            continue
        if key in line:
            k, v = line.split(':')[:2]
            if k != key:
                continue
            val = v.strip()
    return val


def sort_dict_by_value():
    x = {1: [1,2,3,4], 3: [1,2], 4: [1,2,3]}
    sorted_x = sorted(x.items(), key=lambda kv: kv[1], reverse=True)
    net = odict(sorted_x)
    print(net)


if __name__ == '__main__':
    main()
