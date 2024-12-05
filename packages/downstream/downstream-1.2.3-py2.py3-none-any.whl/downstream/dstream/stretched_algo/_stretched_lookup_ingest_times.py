import typing

import numpy as np

from ..._auxlib._bit_floor import bit_floor
from ..._auxlib._bitlen32 import bitlen32
from ..._auxlib._ctz import ctz


def stretched_lookup_ingest_times(
    S: int, T: int
) -> typing.Iterable[typing.Optional[int]]:
    """Ingest time lookup algorithm for stretched curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Yields
    ------
    typing.Optional[int]
        Ingest time of stored item, if any, at buffer sites in index order.
    """
    if T < S:  # Patch for before buffer is filled...
        return (v if v < T else None for v in stretched_lookup_impl(S, S))
    else:  # ... assume buffer has been filled
        return stretched_lookup_impl(S, T)


def stretched_lookup_impl(
    S: int,
    T: typing.Union[int, np.ndarray],
) -> typing.Iterable[typing.Union[int, np.ndarray]]:
    """Implementation detail for `stretched_lookup_ingest_times`."""
    # T < S redirected to T = S by stretched_lookup_ingest_times
    assert (np.asarray(T) >= S).all()

    s = int(S).bit_length() - 1
    t = bitlen32(T) - s  # Current epoch

    blt = bitlen32(t)  # Bit length of t
    epsilon_tau = bit_floor(t << 1) > t + blt  # Correction factor
    tau0 = blt - epsilon_tau  # Current meta-epoch
    tau1 = tau0 + 1  # Next meta-epoch

    M = np.maximum((S >> tau1), 1)  # Num invading segments at current epoch
    w0 = (1 << tau0) - 1  # Smallest segment size at current epoch start
    w1 = (1 << tau1) - 1  # Smallest segment size at next epoch start

    h_ = 0  # Assigned hanoi value of 0th site
    m_p = 0  # Calc left-to-right index of 0th segment (physical segment idx)
    for k in range(S):  # For each site in buffer...
        b_l = ctz(M + m_p)  # Logical bunch index...
        # ... REVERSE fill order (decreasing nestedness/increasing init size r)

        epsilon_w = m_p == 0  # Correction factor for segment size
        w = w1 + b_l + epsilon_w  # Number of sites in current segment

        # Determine correction factors for not-yet-seen data items, Tbar_ >= T
        i_ = (M + m_p) >> (b_l + 1)  # Guess h.v. incidence (i.e., num seen)
        Tbar_k_ = ((2 * i_ + 1) << h_) - 1  # Guess ingest time
        epsilon_h = (Tbar_k_ >= T) * (w - w0)  # Correction factor, h
        epsilon_i = (Tbar_k_ >= T) * (m_p + M - i_)  # Correction factor, i

        # Decode ingest time for ith instance of assigned h.v.
        h = h_ - epsilon_h  # True hanoi value
        i = i_ + epsilon_i  # True h.v. incidence
        yield ((2 * i + 1) << h) - 1  # True ingest time, Tbar_k

        # Update state for next site...
        h_ += 1  # Assigned h.v. increases within each segment
        m_p += h_ == w  # Bump to next segment if current is filled
        h_ *= h_ != w  # Reset h.v. if segment is filled
