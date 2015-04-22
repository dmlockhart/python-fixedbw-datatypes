================================================================================
Fixed-Bitwidth Arithmetic
================================================================================

--------------------------------------------------------------------------------
Bit-Precise Integer Types
--------------------------------------------------------------------------------

- Verilog:
  http://www1.pldworld.com/@xilinx/html/technote/TOOL/MANUAL/21i_doc/data/fndtn/ver/ver4_4.htm
- Chisel:
  https://chisel.eecs.berkeley.edu/chisel-dac2012.pdf
- Xilinx Vivado ap_int/ap_uint:
  http://www.xilinx.com/support/documentation/sw_manuals/xilinx2014_2/ug902-vivado-high-level-synthesis.pdf

Expressions involving only explicitly-sized variables and constants::

  Operation    Verilog              Chisel               PyMTL Bits        ap_int/ap_uint
  -----------  -------------------  -------------------  ----------------  --------------

  i + j        max(L(i),L(j))  @    max(L(i),L(j)) + 1   max(L(i),L(j))    max(L(i),L(j)) + 1
                                                                            + narrower_is_signed(i,j)
  i - j        max(L(i),L(j))  @    max(L(i),L(j)) + 1   max(L(i),L(j))    max(L(i),L(j)) + 1
                                                                            + narrower_is_signed(i,j)
  i * j        max(L(i),L(j))  @    L(i) + L(j)          2*max(L(i),L(j))  L(i) + L(j)
  i / j        max(L(i),L(j))  @    ?                    2*max(L(i),L(j))  L(i) + is_signed(j)
  i % j        max(L(i),L(j))  @    ?                    2*max(L(i),L(j))  if   (sign(i) == sign(j)): min(L(i),L(j))
                                                                           elif (is_signed(i)):       L(j) + 1
  i & j        max(L(i),L(j))  @    max(L(i),L(j))       max(L(i),L(j))    max(L(i),L(j))
  i | j        max(L(i),L(j))  @    max(L(i),L(j))       max(L(i),L(j))    max(L(i),L(j))
  i ^ j        max(L(i),L(j))  @    max(L(i),L(j))       max(L(i),L(j))    max(L(i),L(j))
  i ^~ j       max(L(i),L(j))  @    -                    -                 -
  ~i           L(i)            @    L(i)                 L(i)              L(i)
  i == j       1-bit                ?                    1-bit             Bool
  i !== j      1-bit                ?                    1-bit             Bool
  i && j       1-bit                ?                    1-bit             Bool
  i || j       1-bit                ?                    1-bit             Bool
  i > j        1-bit                ?                    1-bit             Bool
  i >= j       1-bit                ?                    1-bit             Bool
  i < j        1-bit                ?                    1-bit             Bool
  i <= j       1-bit                ?                    1-bit             Bool
  &i           1-bit                ?                    1-bit             1-bit
  |i           1-bit                ?                    1-bit             1-bit
  ^i           1-bit                ?                    1-bit             1-bit
  ~&i          1-bit                ?                    -                 1-bit
  ~|i          1-bit                ?                    -                 1-bit
  ~^i          1-bit                ?                    -                 1-bit
  i >> j       L(i)            @@   L(i) + maxNum( j )   L(i)              L(i)
  i << j       L(i)            @@   L(i) - minNum( j )   L(i)              L(i)
  i ? j : k    max(L(j),L(k))  @@   max(L(j), L(k))      ?                 ?
  {i,...,j}    L(i)+...+L(j)        L(i)+...+L(j)        L(i)+...+L(j)     L(i)+...+L(j)
  {i{j}}       i*L(j)          @@   L(j) * maxNum( i )   -                 ?
  {i{j,...,k}} i*(L(j)+...+L(k))    ?                    -                 ?

Expressions involving unsized contants (indicated using N)::

  Operation    Verilog              Chisel               PyMTL              ap_int/ap_uint
  -----------  -------------------  -------------------  ----------------   ----------------

  i + N        max(L(i), 32)   @    ?                    L(i)               max(L(i),L(N)) + 1
                                                                             + narrower_is_signed(i,N)
  i - N        max(L(i), 32)   @    ?                    L(i)               max(L(i),L(N)) + 1
                                                                             + narrower_is_signed(i,N)
  i * N        max(L(i), 32)   @    ?                    L(i)               L(i) + L(N)
  i / N        max(L(i), 32)   @    ?                    L(i)               L(i) + is_signed(N)
  i % N        max(L(i), 32)   @    ?                    L(i)               if   (sign(i) == sign(N)): min(L(i),L(N))
                                                                            elif (is_signed(i)):       L(N) + 1
  i & N        max(L(i), 32)   @    ?                    L(i)               max(L(i),L(N))
  i | N        max(L(i), 32)   @    ?                    L(i)               max(L(i),L(N))
  i ^ N        max(L(i), 32)   @    ?                    L(i)               max(L(i),L(N))
  i ^~ j       max(L(i), 32)   @    -                    -                  -
  i >> N       L(i)            @@   ?                    L(i)               L(i)
  i << N       L(i)            @@   ?                    L(i)               L(i)

  N + j        max(32, L(j))   @    ?                    L(j)               max(L(N),L(j)) + 1
                                                                             + narrower_is_signed(N,j)
  N - j        max(32, L(j))   @    ?                    L(j)               max(L(N),L(j)) + 1
                                                                             + narrower_is_signed(N,j)
  N * j        max(32, L(j))   @    ?                    L(j)               L(N) + L(j)
  N / j        max(32, L(j))   @    ?                    invalid            L(N) + is_signed(j)
  N % j        max(32, L(j))   @    ?                    invalid            if   (sign(N) == sign(j)): min(L(N),L(j))
                                                                            elif (is_signed(N)):       L(j) + 1
  N & j        max(32, L(j))   @    ?                    L(j)               max(L(N),L(j))
  N | j        max(32, L(j))   @    ?                    L(j)               max(L(N),L(j))
  N ^ j        max(32, L(j))   @    ?                    L(j)               max(L(N),L(j))
  i ^~ j       max(32, L(j))   @    -                    -                  -
  N >> j       L(i)            @@   ?                    invalid            L(N)
  N << j       L(i)            @@   ?                    invalid            L(N)

  i ? N : k    max(32, L(k))   @@   ?                    ?                  ?

Definitions in Python-like pseudocode::

  def is_signed( x ):
    type( x ).is_signed_datatype()

  def narrower_is_signed( i, j ):
    if   L(i) < L(j):
      return is_signed( i ) and not is_signed( j )
    elif L(i) > L(j):
      return is_signed( j ) and not is_signed( i )
    else:
      return ???

  def L( x ):
    if   type( x, BitType   ): return x.nbits
    elif type( x, char      ): return 8
    elif type( x, short     ): return 16
    elif type( x, int       ): return 32
    elif type( x, long      ): return 32
    elif type( x, long long ): return 64


Verilog self-determined and context-determined operations are described
below:

Self-determined (no marker): bitwidths of RHS operands are never extended.
The bitwidth of the RHS expression depends only on the RHS.

Context-determined (@): bitwidths of RHS operands are extended depending
on the bitwidth of other RHS variables and the LHS variable. The bitwidth
of the RHS expression is therefore dependent on all RHS and LHS variables.

Partially context-determined (@@): the bitwdiths of some RHS are extended
depending on the bitwidth of other RHS variables and the LHS variable.
The bitwidth of the RHS expression is therefore depends on some RHS
variables and the LHS variable. In the above table the ``j`` variable is
self-determined, but all other variables are context-determined.


--------------------------------------------------------------------------------
Bit-Precise Fixed-Point Types
--------------------------------------------------------------------------------

- Xilinx Vivado ap_fixed/ap_ufixed:
  http://www.xilinx.com/support/documentation/sw_manuals/xilinx2014_2/ug902-vivado-high-level-synthesis.pdf

Expressions involving only explicitly-sized variables and constants::

  W = I + F

  Operation     PyMTL FixPoint    ap_int/ap_uint
  -----------   ----------------  --------------

  i + j         ?                 W = max(L(i),  L(j)  ) + 1 + narrower_is_signed(i,j)
                                  I = max(L(i.I),L(j.I)) + 1 + narrower_is_signed(i,j)

  i - j         ?                 W = max(L(i),  L(j)  ) + 1 + narrower_is_signed(i,j)
                                  I = max(L(i.I),L(j.I)) + 1 + narrower_is_signed(i,j)

  i * j         ?                 W = L(i)   + L(j)
                                  I = L(i.I) + L(j.I)

  i / j         ?                 I = L(i.F) + L(j.I)
                                  F = L(i)   + L(j.F)

  i % j         ?                 ?

  i & j         ?                 I = max(L(i.I),L(j.I))
                                  F = max(L(i.F),L(j.F))
  i | j         ?                 I = max(L(i.I),L(j.I))
                                  F = max(L(i.F),L(j.F))
  i ^ j         ?                 I = max(L(i.I),L(j.I))
                                  F = max(L(i.F),L(j.F))

  ~i            ?                 W = L(i)
                                  I = L(i.I)

  i >> j        ?                 W = L(i)
                                  I = L(i.I)

  i << j        ?                 L(i)
                                  I = L(i.I)

  {i,...,j}     ?                 L(i)+...+L(j)
  {i{j}}        ?                 ?
  {i{j,...,k}}  ?                 ?

