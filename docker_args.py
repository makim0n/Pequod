#!/usr/bin/python3

import argparse

def arguments_menu():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--container", help="Pull a remote image without authentication")
    parser.add_argument("-a","--authentication", help="Pull a remote image with authentication")
    parser.add_argument("-l","--local-container", help="Get a local image")
    parser.add_argument("-i","--item", help="Search a specific item")
    parser.add_argument("-e", "--extract", help="Extract specific file")
    args = parser.parse_args()
    return args
