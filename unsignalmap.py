#!/bin/python3

import sys
import struct

Gpio = struct.Struct('<I 20s')

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} [DEVICE_TREE_SOURCE]")
		exit(1)

	signalmap_key = "signalmap"

	with open(sys.argv[1]) as dts:

		signalmap_data = None

		for line in dts:
			line = line.strip()
			if line.startswith(signalmap_key):
				hexs = line[len(signalmap_key) + 4: -2].split(' ')
				signalmap_data = bytearray()
				for hexnum in hexs:
					hexnum = hexnum[2:]
					while len(hexnum) < 8:
						hexnum = "0" + hexnum
					signalmap_data = signalmap_data + bytearray.fromhex(hexnum)

		if signalmap_data is not None:
			for i in range(0, int(len(signalmap_data) / 24)):
				entry = signalmap_data[i * 24: (i + 1) * 24]
				gpio = Gpio.unpack(entry)
				print("{:20} {}".format(gpio[1].decode("ascii"), gpio[0]))
