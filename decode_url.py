#!/usr/bin/python


def decode_url(catalog_name_url):
    if catalog_name_url.find("_") == -1: 
        decoded_name = catalog_name_url.replace(' ', '_')
    else:
        decoded_name = catalog_name_url.replace('_', ' ')
    return decoded_name

avar = decode_url(raw_input())

print "Straight outta print", avar
