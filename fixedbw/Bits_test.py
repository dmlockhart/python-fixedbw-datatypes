#=======================================================================
# Bits_test.py
#=======================================================================
# Tests for the Bits class.

import pytest

from   Bits import Bits

#-----------------------------------------------------------------------
# test_return_type
#-----------------------------------------------------------------------
def test_return_type():

  x = Bits( 8 )( 0b1100 )

  Bits1 = Bits(1)
  Bits4 = Bits(4)

  assert isinstance( x.uint(), int  )
  assert isinstance( x.int(),  int  )
  assert isinstance( x[1:2],   Bits1 )
  assert isinstance( x[0:4],   Bits4 )
  assert isinstance( x[2],     Bits1 )

#-----------------------------------------------------------------------
# test_constructor
#-----------------------------------------------------------------------
def test_constructor():

  Bits4 = Bits(4)

  assert Bits4(  2 ).uint() == 2
  assert Bits4(  4 ).uint() == 4
  assert Bits4( 15 ).uint() == 15

  assert Bits4( -2 ).uint() == 0b1110
  assert Bits4( -4 ).uint() == 0b1100

  # Bits(N) returns a class, Bits(N)(value) creates an instance!

  with pytest.raises( AssertionError ):
    assert Bits4 == Bits( 4 )( 0 )

  with pytest.raises( AssertionError ):
    assert Bits(4) == Bits( 4 )( 0 )

  # Bits(N) returns a class, not an instance!
  # Does not have methods until instantiated!

  with pytest.raises( TypeError ):
    assert Bits4.uint() == 0

  with pytest.raises( TypeError ):
    assert Bits(4).uint() == 0

  # Sanity checks of subclassing. Note that all types (classes) are
  # objects, but object instances are objects, but not **not** types!

  assert     isinstance( Bits4,      type   )
  assert     isinstance( Bits4,      object )
  assert not isinstance( Bits4(0),   type   )
  assert     isinstance( Bits4(0),   object )

  assert     isinstance( Bits(4),    type   )
  assert     isinstance( Bits(4),    object )
  assert not isinstance( Bits(4)(0), type   )
  assert     isinstance( Bits(4)(0), object )

#-----------------------------------------------------------------------
# test_constructor_bounds_checking
#-----------------------------------------------------------------------
def test_constructor_bounds_checking():

  Bits( 4 )( 15 )
  with pytest.raises( AssertionError ):
    Bits( 4 )( 16 )

  Bits( 4 )( -8 )
  with pytest.raises( AssertionError ):
    Bits( 4 )( -9 )
  with pytest.raises( AssertionError ):
    Bits( 4 )( -16 )

  Bits( 1 )( 0 )
  Bits( 1 )( 1 )
  with pytest.raises( AssertionError ):
    Bits( 1 )( -1 )
  with pytest.raises( AssertionError ):
    Bits( 1 )( -2 )

#-----------------------------------------------------------------------
# test_construct_from_bits
#-----------------------------------------------------------------------
def test_construct_from_bits():

  assert Bits( 4 )( Bits(4)( -2) ).uint() == 0b1110
  assert Bits( 4 )( Bits(4)( -4) ).uint() == 0b1100

  a = Bits( 8 )( 5 )
  assert a                              == 0x05
  assert Bits( 16 )( a ).uint()         == 0x0005
  assert Bits( 16 )( ~a + 1 ).uint()    == 0x00FB
  b = Bits( 32 )( 5 )
  assert b                              == 0x00000005
  assert Bits( 32 )( ~b + 1 ).uint()    == 0xFFFFFFFB
  c = Bits( 32 )( 0 )
  assert c                              == 0x00000000
  assert Bits( 32 )( ~c )               == 0xFFFFFFFF
  assert Bits( 32 )( ~c + 1 )           == 0x00000000
  d = Bits( 4 )( -1 )
  assert Bits( 8 )( d )                 == 0x0F

  assert Bits( Bits(4)(4) )( 1 ).uint() == 1

#-----------------------------------------------------------------------
# test_int
#-----------------------------------------------------------------------
def test_int():

  assert Bits( 4 )(  0 ).int() == 0
  assert Bits( 4 )(  2 ).int() == 2
  assert Bits( 4 )(  4 ).int() == 4
  assert Bits( 4 )( 15 ).int() == -1
  assert Bits( 4 )( -1 ).int() == -1
  assert Bits( 4 )( -2 ).int() == -2
  assert Bits( 4 )( -4 ).int() == -4
  assert Bits( 4 )( -8 ).int() == -8

#-----------------------------------------------------------------------
# test_uint
#-----------------------------------------------------------------------
def test_uint():

  assert Bits( 4 )(  0 ).uint() == 0
  assert Bits( 4 )(  2 ).uint() == 2
  assert Bits( 4 )(  4 ).uint() == 4
  assert Bits( 4 )( 15 ).uint() == 15
  assert Bits( 4 )( -1 ).uint() == 15
  assert Bits( 4 )( -2 ).uint() == 14
  assert Bits( 4 )( -4 ).uint() == 12

#-----------------------------------------------------------------------
# test_neg_assign
#-----------------------------------------------------------------------
def test_neg_assign():

  x = Bits( 4 )( -1 )
  assert x        == 0b1111
  assert x.uint() == 0b1111
  x = Bits( 4 )( -2 )
  assert x        == 0b1110
  assert x.uint() == 0b1110

#-----------------------------------------------------------------------
# test_get_single_bit
#-----------------------------------------------------------------------
def test_get_single_bit():

  x = Bits( 4 )( 0b1100 )
  assert x[3] == 1
  assert x[2] == 1
  assert x[1] == 0
  assert x[0] == 0

#-----------------------------------------------------------------------
# test_set_single_bit
#-----------------------------------------------------------------------
def test_set_single_bit():

  x = Bits( 4 )( 0b1100 )
  x[3] = 0
  assert x.uint() == 0b0100
  x[2] = 1
  assert x.uint() == 0b0100
  x[1] = 1
  assert x.uint() == 0b0110

#-----------------------------------------------------------------------
# test_single_bit_bounds_checking
#-----------------------------------------------------------------------
def test_single_bit_bounds_checking():

  x = Bits( 4 )( 0b1100 )
  with pytest.raises( IndexError ):
    assert x[-1] == 1
  with pytest.raises( IndexError ):
    assert x[8] == 1
  with pytest.raises( IndexError ):
    x[-1] = 1
  with pytest.raises( IndexError ):
    x[4] = 1
  with pytest.raises( AssertionError ):
    x[0] = 2
  with pytest.raises( AssertionError ):
    x[3] = -1

#-----------------------------------------------------------------------
# test_get_slice
#-----------------------------------------------------------------------
def test_get_slice():

  x = Bits( 4 )( 0b1100 )
  assert x[:] == 0b1100
  assert x[2:4] == 0b11
  assert x[0:1] == 0b0
  assert x[1:3] == 0b10
  # check open ended ranges
  assert x[1:] == 0b110
  assert x[:3] == 0b100

#-----------------------------------------------------------------------
# test_set_slice
#-----------------------------------------------------------------------
def test_set_slice():

  x = Bits( 4 )( 0b1100 )
  x[:] = 0b0010
  assert x.uint() == 0b0010
  x[2:4] = 0b11
  assert x.uint() == 0b1110
  x[0:1] = 0b1
  assert x.uint() == 0b1111
  x[1:3] = 0b10
  assert x.uint() == 0b1101
  # check open ended ranges
  x[1:] = 0b001
  assert x.uint() == 0b0011
  x[:3] = 0b110
  assert x.uint() == 0b0110

  with pytest.raises( AssertionError ):
    x[1:3] = 0b110

#-----------------------------------------------------------------------
# test_slice_bounds_checking
#-----------------------------------------------------------------------
def test_slice_bounds_checking():

  x = Bits( 4 )( 0b1100 )
  with pytest.raises( IndexError ):
    assert x[1:5]  == 0b10
  with pytest.raises( IndexError ):
    assert x[-1:2] == 0b10
  with pytest.raises( IndexError ):
    assert x[2:1]  == 0b10
  with pytest.raises( IndexError ):
    x[1:5]  = 0b10
  with pytest.raises( IndexError ):
    x[-1:2] = 0b10
  with pytest.raises( IndexError ):
    x[2:1]  = 0b10

  # FIXED
  # Bits objects constructed with another Bits object provided as a value
  # parameter end up having problems when writing to slices.  This is
  # because the mask used when writing to a subslice is often a negative
  # int in Python, and we don't allow operations on Bits to be performed
  # with negative values.  Current workaround is to force the value param
  # for the Bits constructor to be an int or a long.
  #with pytest.raises( AssertionError ):
  y      = Bits(4)( Bits(4)(0) )
  y[1:3] = 1


#-----------------------------------------------------------------------
# test_eq
#-----------------------------------------------------------------------
def test_eq():

  x = Bits( 4 )( 0b1010 )
  assert x.uint() == x.uint()
  # Compare objects by value, not id
  assert x == x
  # Check the value
  assert x.uint() == 0b1010
  assert x.uint() == 0xA
  assert x.uint() == 10
  # Checking the equality operator
  assert x == 0b1010
  assert x == 0xA
  assert x == 10
  # Checking comparison with another bit container
  y = Bits( 4 )( 0b1010 )
  assert x.uint() == y.uint()
  assert x == y
  y = Bits( 8  )( 0b1010 )
  assert x.uint() == y.uint()
  # TODO: How should equality between Bits objects work?
  #       Just same value or same value and width?
  #assert x == y
  # Check the negatives
  x = Bits( 4 )( -1 )
  assert x.uint() == 0b1111
  assert x.uint() == 0xF
  assert x.uint() == 15
  # Checking the equality operator
  assert x == 0b1111
  assert x == 0xF
  assert x == 15
  assert x.uint() == Bits(4)(-1).uint()
  assert x == Bits( 4 )( -1 ).uint()
  assert 15 == x

  assert not x == None
  assert not Bits( 4 )( 0 ) == None

#-----------------------------------------------------------------------
# test_ne
#-----------------------------------------------------------------------
def test_ne():

  x = Bits( 4 )( 0b1100 )
  y = Bits( 4 )( 0b0011 )
  # TODO: check width?
  assert x.uint() != y.uint()
  assert x != y
  # added for bug
  z = Bits( 1 )( 0 )
  assert z.uint() != 1L
  assert z != 1L
  assert 5 != x

  assert z != None
  assert Bits( 4 )( 0 ) != None

#-----------------------------------------------------------------------
# test_compare_neg_assert
#-----------------------------------------------------------------------
def test_compare_neg_assert():

  x = Bits( 4 )( -2 )
  # We don't allow comparison with negative numbers,
  # although you can construct a new Bits object with one...
  with pytest.raises( AssertionError ):
    assert x != -1
  with pytest.raises( AssertionError ):
    assert x == -2
  with pytest.raises( AssertionError ):
    assert x >  -3
  with pytest.raises( AssertionError ):
    assert x >= -3
  with pytest.raises( AssertionError ):
    assert x <  -1
  with pytest.raises( AssertionError ):
    assert x >= -1
  assert x != Bits( 4 )( -1 )
  assert x == Bits( 4 )( -2 )
  assert x >  Bits( 4 )( -3 )
  assert x >= Bits( 4 )( -3 )
  assert x <  Bits( 4 )( -1 )
  assert x <= Bits( 4 )( -1 )

#-----------------------------------------------------------------------
# test_compare_uint_neg
#-----------------------------------------------------------------------
def test_compare_uint_neg():

  x = Bits( 4 )( 2 )
  assert x.uint() != -1
  assert x.uint()  > -1
  assert x.uint() >= -1

#-----------------------------------------------------------------------
# test_compare_int_neg
#-----------------------------------------------------------------------
def test_compare_int_neg():

  x = Bits( 4 )( -2 )
  assert x.int() == -2
  assert x.int()  < -1
  assert x.int() <= -1

#-----------------------------------------------------------------------
# test_lt
#-----------------------------------------------------------------------
def test_lt():

  x = Bits( 4 )( 0b1100 )
  y = Bits( 4 )( 0b0011 )
  assert y.uint() < x.uint()
  assert y.uint() < 10
  assert y < x.uint()
  assert y < 10
  assert y < x
  assert 1 < y

#-----------------------------------------------------------------------
# test_gt
#-----------------------------------------------------------------------
def test_gt():

  x = Bits( 4 )( 0b1100 )
  y = Bits( 4 )( 0b0011 )
  assert x.uint() > y.uint()
  assert x.uint() > 2
  assert x > y.uint()
  assert x > 2
  assert x > y
  assert 9 > y

#-----------------------------------------------------------------------
# test_lte
#-----------------------------------------------------------------------
def test_lte():

  x = Bits( 4 )( 0b1100 )
  y = Bits( 4 )( 0b0011 )
  z = Bits( 4 )( 0b0011 )
  assert y.uint() <= x.uint()
  assert y.uint() <= 10
  assert y.uint() <= z.uint()
  assert y.uint() <= 0b0011
  assert y <= x.uint()
  assert y <= 10
  assert y <= z.uint()
  assert y <= 0b0011
  assert y <= x
  assert y <= z
  assert z <= x
  assert z <= z
  assert 1 <= y
  assert 3 <= y

#-----------------------------------------------------------------------
# test_gte
#-----------------------------------------------------------------------
def test_gte():

  x = Bits( 4 )( 0b1100 )
  y = Bits( 4 )( 0b0011 )
  z = Bits( 4 )( 0b1100 )
  assert x.uint() >= y.uint()
  assert x.uint() >= 2
  assert x.uint() >= z.uint()
  assert x.uint() >= 0b1100
  assert x >= y.uint()
  assert x >= 2
  assert x >= z.uint()
  assert x >= 0b1100
  assert x >= y
  assert x >= z
  assert z >= y
  assert z >= x
  assert x >= x
  assert 5 >= y
  assert 3 <= y

#-----------------------------------------------------------------------
# test_invert
#-----------------------------------------------------------------------
def test_invert():

  x = Bits( 4 )( 0b0001 )
  assert ~x == 0b1110
  x = Bits( 4 )( 0b1001 )
  assert ~x == 0b0110
  x = Bits( 16 )( 0b1111000011110000 )
  assert ~x == 0b0000111100001111

#-----------------------------------------------------------------------
# test_add
#-----------------------------------------------------------------------
def test_add():

  x, y = [Bits(4)(4)] * 2

  # simple (no overflow condition)
  assert x + y          == 8
  assert x + Bits(4)(4) == 8
  assert x + 4          == 8

  # don't extend bitwidth if added to int: overflow!
  assert (x + 14).nbits == x.nbits
  assert x + 14 == 2 and ( x + 14).nbits == 4
  assert 14 + x == 2 and (14 +  x).nbits == 4

  # infer wider bitwidth if both operands are Bits: no overflow possible!
  y = Bits( 4 )( 14 )
  assert x + y == 18 and (x + y).nbits == 5
  assert y + x == 18 and (x + y).nbits == 5

  a = Bits( 4 )( 1 )
  b = Bits( 4 )( 1 )
  c = Bits( 1 )( 1 )
  assert a + b + 1 == 3
  assert a + b + c == 3
  assert c + b + a == 3

#-----------------------------------------------------------------------
# test_sub
#-----------------------------------------------------------------------
def test_sub():

  x,y = [Bits(4)(5), Bits(4)(4)]

  # simple (no overflow condition)
  assert x - y          == 1
  assert x - Bits(4)(4) == 1
  assert x - 4          == 1

  y = Bits(4)(5)
  assert x - y == 0 and (x - y).nbits == 5
  assert x - 5 == 0 and (x - 5).nbits == 4

  # infer wider bitwidth if both operands are Bits: no overflow possible!
  y = Bits(4)(7)
  assert x - y == 0b11110 and (x - y).nbits == 5
  assert y - x == 0b00010 and (x - y).nbits == 5

  # don't extend bitwidth if added to int: overflow!
  assert x - 7 ==  0b1110 and (x - 7).nbits == 4
  assert 7 - x ==  0b0010 and (7 - x).nbits == 4
  assert 9 - x ==  0b0100 and (9 - x).nbits == 4

#-----------------------------------------------------------------------
# test_lshift
#-----------------------------------------------------------------------
def test_lshift():

  x = Bits( 8 )( 0b1100 )
  y = Bits( 8 )( 4 )
  assert x << y == 0b11000000
  assert x << 4 == 0b11000000
  assert x << 6 == 0b00000000
  assert y << x == 0b00000000
  assert y << 0 == 0b00000100
  assert y << 1 == 0b00001000

#-----------------------------------------------------------------------
# test_rshift
#-----------------------------------------------------------------------
def test_rshift():

  x = Bits( 8 )( 0b11000000 )
  y = Bits( 8 )( 4 )
  assert x >> y  == 0b00001100
  assert x >> 7  == 0b00000001
  assert x >> 8  == 0b00000000
  assert x >> 10 == 0b00000000
  x = Bits( 8 )( 2 )
  assert y >> x == 0b00000001
  assert y >> 0 == 0b00000100
  assert y >> 2 == 0b00000001
  assert y >> 5 == 0b00000000

#-----------------------------------------------------------------------
# test_and
#-----------------------------------------------------------------------
def test_and():

  x = Bits( 8 )( 0b11001100 )
  y = Bits( 8 )( 0b11110000 )
  assert x & y      == 0b11000000
  assert x & 0b1010 == 0b00001000
  assert 0b1010 & x == 0b00001000

#-----------------------------------------------------------------------
# test_or
#-----------------------------------------------------------------------
def test_or():

  x = Bits( 8 )( 0b11001100 )
  y = Bits( 8 )( 0b11110000 )
  assert x | y      == 0b11111100
  assert x | 0b1010 == 0b11001110
  assert 0b1010 | x == 0b11001110

#-----------------------------------------------------------------------
# test_xor
#-----------------------------------------------------------------------
def test_xor():

  x = Bits( 8 )( 0b11001100 )
  y = Bits( 8 )( 0b11110000 )
  assert x ^ y      == 0b00111100
  assert x ^ 0b1010 == 0b11000110
  assert 0b1010 ^ x == 0b11000110
  a = Bits( 1 )( 1 )
  b = Bits( 1 )( 0 )
  c = Bits( 1 )( 1 )
  assert ( a ^ b ) ^ c == 0

#-----------------------------------------------------------------------
# test_mult
#-----------------------------------------------------------------------
def test_mult():

  x = Bits( 8 )( 0b00000000 )
  y = Bits( 8 )( 0b00000000 )
  assert x * y == 0b0000000000000000
  assert x * 0b1000 == 0b0000000000000000
  x = Bits( 8 )( 0b11111111 )
  y = Bits( 8 )( 0b11111111 )
  assert x * y == 0b0000000000000001111111000000001
  assert x * 0b11111111 == 0b0000000000000001111111000000001
  assert 0b11111111 * x == 0b0000000000000001111111000000001

  # TODO: Currently fails as the second operand is larger than the Bits
  # object x. Should update the test when we define the behaviour
  #assert x * 0b1111111111 == 0b0000000000000001111111000000001

  y = Bits( 8 )( 0b10000000 )
  assert x * y == 0b0000000000000000111111110000000

#-----------------------------------------------------------------------
# test_str
#-----------------------------------------------------------------------
def test_str():

  assert Bits(  4 )(        0x2 ).__str__() == "2"
  assert Bits(  8 )(       0x1f ).__str__() == "1f"
  assert Bits( 32 )( 0x0000beef ).__str__() == "0000beef"
  # FIXED
  # Bits objects constructed with another Bits object provided as a value
  # parameter end up having problems when printed. This is because the
  # internal ._uint field is expected to be an int/long, but is instead
  # a Bits object, which cannot be formatted as expected. Current
  # workaround is to force the value param for the Bits constructor to be
  # an int or a long.
  #with pytest.raises( ValueError ):
  #with pytest.raises( AssertionError ):
  #  assert Bits( 4 )( Bits(32)(2) ).__str__() == "2"
  assert Bits( 4 )( Bits(32)(2) ).__str__() == "2"

#-----------------------------------------------------------------------
# test_index_array
#-----------------------------------------------------------------------
def test_index_array():

  data = range( 2**4 )

  # Indexing into an array
  x = Bits( 4 )( 3  )
  assert data[ x ] == 3

  # Note, this converts -2 to unsigned, so 14!
  y = Bits( 4 )( -2 )
  assert data[ y ] == 14

  # Larger bitwidths work as long as the list is big enough
  a = Bits( 8 )( 4  )
  assert data[ a ] == 4

  # If not, regular indexing error
  b = Bits( 8 )( 20 )
  with pytest.raises( IndexError ):
    data[ b ]

  # Same with negative that become out of range when converted to unsigned
  c = Bits( 8 )( -1 )
  with pytest.raises( IndexError ):
    data[ c ]

#-----------------------------------------------------------------------
# test_index_bits
#-----------------------------------------------------------------------
def test_index_bits():

  data = Bits( 8 )( 0b11001010 )

  # Indexing into a bits
  x = Bits( 4 )( 3  )
  assert data[ x ] == 1

  # Note, this converts -8 to unsigned, so 8! Out of range!
  y = Bits( 4 )( -8 )
  with pytest.raises( IndexError ):
    data[ y ]

  # Larger bitwidths work as long as the list is big enough
  a = Bits( 8 )( 4  )
  assert data[ a ] == 0

  # If not, regular indexing error
  b = Bits( 8 )( 20 )
  with pytest.raises( IndexError ):
    data[ b ]

  # Same with negative that become out of range when converted to unsigned
  c = Bits( 8 )( -1 )
  with pytest.raises( IndexError ):
    data[ c ]

#-----------------------------------------------------------------------
# test_slice_bits
#-----------------------------------------------------------------------
def test_slice_bits():

  data = Bits( 8 )( 0b1101 )

  # Indexing into a bits
  x = Bits( 4 )( 2  )
  assert data[ : ]   == 0b1101
  assert data[x: ]   == 0b11
  assert data[ :x]   == 0b01
  with pytest.raises( IndexError ):
    assert data[x:x] == 0b1
