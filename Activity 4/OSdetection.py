#!/usr/bin/env python2
import ping


def main():
    file_name = raw_input("Name of the input file: ")
    input_file = open(file_name, "r")
    ip_addrs = input_file.readlines()
    for ip_addr in ip_addrs:
        mix = ping.do_one(ip_addr, 3)
        if mix == None:
            continue
        delay, ttl = mix
        if ttl <= 64:
            print "%s is running Windows" % ip_addr
        else:
            print "%s is running Linux" % ip_addr


if __name__ == '__main__':
    main()
