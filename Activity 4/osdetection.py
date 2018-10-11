#!/usr/bin/env python

import ping


def main():
    file_name = raw_input("Name of the input file: ")
    input_file = open(file_name, "r")
    ip_addrs = input_file.readlines()
    for ip_addr in ip_addrs:
        if ip_addr[-1] == "\n":
            ip_addr = ip_addr[:-1]
        try:
            mix = ping.do_one(ip_addr, 3)
        except:
            print "{ip} could not be reached".format(ip=ip_addr)
            continue
        if mix == None:
            print "{ip} could not be reached".format(ip=ip_addr)
            continue
        delay, ttl = mix
        if (ttl > 64) and (ttl<=128):
            print "%s is running Windows" % ip_addr
        else:
            print "%s is running Linux" % ip_addr


if __name__ == '__main__':
    main()