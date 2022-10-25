#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2022.10.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


def to_hex(value: int) -> str:
	if(value > 255):
		return "FF"
	if(value <= 0):
		return "00"

	return f"{str(hex(value // 16))[2:]}{str(hex(value % 16))[2:]}"
