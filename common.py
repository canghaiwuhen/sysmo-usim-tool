#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User interface parts that are common for all tools

(C) 2017 by Sysmocom s.f.m.c. GmbH
All Rights Reserved

Author: Philipp Maier

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from utils import *
import sys, getopt

COMMON_GETOPTS = "hfa:J:nN:lL:kK:tT:oO:C:"
COMMON_GETOPTS_LONG = ["help", "force", "adm1=", "set-imsi", "mnclen", "set-mnclen", "milenage", "set-milenage", "ki", "set-ki=", "auth", "set-auth=", "opc", "set-op=", "set-opc="]

# Parse common commandline options and keep them as flags
class Common():

	sim = None

	show_helptext = None
	force = False
	adm1 = None
	write_imsi = None
	write_mnclen = None
	show_mnclen = None
	show_milenage = False
	write_milenage = None
	show_ki = None
	write_ki = None
	show_auth = False
	write_auth = None
	show_opc = False
	write_op = None
	write_opc = None


	def __init__(self, argv, getopts, getopts_long):

		self._banner()

		# Analyze commandline options
		try:
			opts, args = getopt.getopt(argv, COMMON_GETOPTS + getopts,
				COMMON_GETOPTS_LONG + getopts_long)
		except getopt.GetoptError:
			print " * Error: Invalid commandline options"
			sys.exit(2)

		# Set flags for common options
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				self.__common_helptext()
				sys.exit(0)
			elif opt in ("-f", "--force"):
				self.force = True
			elif opt in ("-a", "--adm1"):
				self.adm1 = ascii_to_list(arg)
			elif opt in ("-J", "--set-imsi"):
				self.write_imsi = asciihex_to_list(pad_asciihex(arg, True, '9'))
			elif opt in ("-n", "--mnclen"):
				self.show_mnclen = True
			elif opt in ("-N", "--set-mnclen"):
				self.write_mnclen = asciihex_to_list(arg)
			elif opt in ("-l", "--milenage"):
				self.show_milenage = True
			elif opt in ("-L", "--set-milenage"):
				self.write_milenage = asciihex_to_list(arg)
			elif opt in ("-k", "--ki"):
				self.show_ki = True
			elif opt in ("-K", "--set-ki"):
				self.write_ki = asciihex_to_list(arg)
			elif opt in ("-t", "--auth"):
				self.show_auth = True
			elif opt in ("-T", "--set-auth"):
				self.write_auth = arg.split(':',1)
			elif opt in ("-o", "--opc"):
				self.show_opc = True
			elif opt in ("-O", "--set-op"):
				self.write_op = asciihex_to_list(arg)
			elif opt in ("-C", "--set-opc"):
				self.write_opc = asciihex_to_list(arg)


		# Check for ADM1 key
		if not self.adm1:
			print " * Error: adm1 parameter missing -- exiting..."
			print ""
			sys.exit(1)

		# Set flags for specific options
		self._options(opts)

		# Initialize
		self._init()

		# Execute tasks
		self.__common_execute()


	# Print the part of the helptext that is common for all tools
	def __common_helptext(self):
		print(" * Commandline options:")
		print("   -h, --help ..................... Show this screen")
		print("   -f, --force .................... Enforce authentication after failure")
		print("   -a, --adm1 CHV ................. Administrator PIN (e.g 55538407)")
		print("   -J, --set-imsi ................. Set IMSI value")
		print("   -n, --mnclen ................... Show MNC length value")
		print("   -N, --set-mnclen ............... Set MNC length value")
		print("   -l, --milenage ................. Show milenage parameters")
		print("   -L, --set-milenage HEXSTRING ... Set milenage parameters")
		print("   -k, --ki ....................... Show KI value")
		print("   -K, --set-ki ................... Set KI value")
		print("   -t, --auth ..................... Show Authentication algorithms")
		print("   -T, --set-auth 2G:3G ........... Set 2G/3G Auth algo (e.g. COMP128v1:COMP128v1)")
		print("   -o, --opc ...................... Show OP/c configuration")
		print("   -O, --set-op HEXSTRING ......... Set OP value")
		print("   -C, --set-opc HEXSTRING ........ Set OPc value")
		self._helptext()


	# Execute common tasks
	def __common_execute(self):

		# Autnetnication is a primary task that must always run before
		# any other task is carried out
		if self.sim.admin_auth(self.adm1, self.force) == False:
			exit(1)

		# First run the card specific tasks
		self._execute()

		# And then the common tasks
		if self.write_imsi:
			self.sim.write_imsi(self.write_imsi)

		if self.show_mnclen:
			self.sim.show_mnclen()

		if self.write_mnclen:
			self.sim.write_mnclen(self.write_mnclen)

		if self.write_milenage:
			self.sim.write_milenage_params(self.write_milenage)

		if self.show_milenage:
			self.sim.show_milenage_params()

		if self.write_ki:
			self.sim.write_ki_params(self.write_ki)

		if self.show_ki:
			self.sim.show_ki_params()

		if self.show_auth:
			self.sim.show_auth_params()

		if self.write_auth:
			self.sim.write_auth_params(self.write_auth[0], self.write_auth[1])

		if self.show_opc:
			self.sim.show_opc_params()

		if self.write_op:
			self.sim.write_opc_params(0, self.write_op)

		if self.write_opc:
			self.sim.write_opc_params(1, self.write_opc)

		print "Done!"
