#!/usr/bin/python

from sys import argv
from optparse import OptionParser
import os, random, string

def randPass(length=13,quantity=1):
    """ @param length
        @param quantity
    """
    if length == None:
        length = 13
    if quantity == None:
        quantity = 1

    
    chars =  string .ascii_letters +  string .digits +  '!@#$%^&*._-'
    random.seed = (os.urandom( 1024 ))
    
    for k in range(0,int(quantity)):        
        print   '' .join(random.choice(chars)  for  i  in  range(int(length)))


parser = OptionParser()
parser.add_option("-l", type="int", dest="length")
parser.add_option("-c", type="int", dest="quantity")

(options, args) = parser.parse_args()

length = options.length
quantity = options.quantity

if length and quantity:
    randPass(length,quantity)
elif length and not quantity:
    randPass(length)
else:
    randPass(13,quantity)
