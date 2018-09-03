#!/usr/bin/python

import distribution

if __name__ == '__main__':
    central = distribution.Server()
    central.check_if_directory_is_empty()
