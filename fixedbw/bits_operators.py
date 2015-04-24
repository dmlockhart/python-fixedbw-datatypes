#=======================================================================
# bit_operators.py
#=======================================================================

import math
import operator

from Bits import Bits
from Bits import _get_nbits

#-----------------------------------------------------------------------
# nbits
#-----------------------------------------------------------------------
def nbits( value ):
  'Return the bitwidth needed to store an integer of size value.'
  return _get_nbits( value )

#-----------------------------------------------------------------------
# clog2
#-----------------------------------------------------------------------
def clog2( value ):
  'Return the bitwidth needed to index into a list of size value.'
  assert value > 0
  return int( math.ceil( math.log( value, 2 ) ) )

#-----------------------------------------------------------------------
# concat
#-----------------------------------------------------------------------
def concat( *bits_objects  ):
  'Return the concatenation all Bits parameters as a new Bits object.'

  # Calculate total new bitwidth
  nbits = sum( [ x.nbits for x in bits_objects ] )

  # Create new Bits and add each bits from bits_list to it
  concat_bits = Bits(nbits)(0)

  begin = 0
  for bits in reversed( bits_objects ):
    concat_bits[ begin : begin+bits.nbits ] = bits
    begin += bits.nbits

  return concat_bits

#-----------------------------------------------------------------------
# zext
#-----------------------------------------------------------------------
def zext( bits, new_width ):
  'Return a zero-extended verion of the provided Bits object.'
  return Bits(new_width)(bits.uint())

#-----------------------------------------------------------------------
# sext
#-----------------------------------------------------------------------
def sext( bits, new_width ):
  'Return a sign-extended verion of the provided Bits object.'
  return Bits(new_width)(bits.int())

#-----------------------------------------------------------------------
# reduce_and
#-----------------------------------------------------------------------
def reduce_and( bits ):
  'Return a Bits1 with anded value of each individual bit in Bits.'
  return Bits(1)(
    reduce(operator.and_, (bits[x] for x in xrange(bits.nbits)) )
  )

#-----------------------------------------------------------------------
# reduce_or
#-----------------------------------------------------------------------
def reduce_or( bits ):
  'Return a Bits1 with the or-ed value of each individual bit in Bits.'
  return Bits(1)(
    reduce(operator.or_, (bits[x] for x in xrange(bits.nbits)) )
  )

#-----------------------------------------------------------------------
# reduce_xor
#-----------------------------------------------------------------------
def reduce_xor( bits ):
  'Return a Bits1 with the xored value of each individual bit in Bits.'

  # verilog iterates through MSB to LSB, so we must reverse iteration
  bits_iterator = reversed(xrange(bits.nbits))

  return Bits(1)(
    reduce(operator.xor, (bits[x] for x in bits_iterator))
  )
