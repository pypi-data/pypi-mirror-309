import numpy as np
import scipy as sp
from lazylinop import LazyLinOp


_valid_norms = ['ortho', None, '1/n']


def rfft(N, n: int = None,
         norm: str = 'ortho', workers: int = None, fft_output=True):
    r"""
    Builds a Discrete Fourier Transform (DFT) :class:`.LazyLinOp` for real
    input.

    Operator dimensions:
        - ``fft_output=True``: $n \times N$.
        - ``fft_output=False``: $L \times N$ with $L = (n + 1) / 2$ if $n$ is
          odd, $L = (n / 2) + 1$ otherwise (take $n = N$ if $n$ is ``None``).

    `SciPy real FFT <https://docs.scipy.org/doc/scipy /reference/generated/
    scipy.fft.rfft.html>`_ is used as underlying implementation.

    To compute the inverse real FFT, simply use ``rfft(...).inv()``
    (see example below). It works for any ``norm``.

    Args:
        N: ``int``
            Size of the input ($N > 0$).
        n: ``int``, optional
            Crop/zero-pad the input to get a signal of size ``n``
            to apply the DFT on. ``None`` (default) means ``n=N``.
        norm: ``str``, optional
            Normalization mode:
            ``'ortho'`` (default), ``None`` or ``'1/n'``.
            See :func:`.fft` for more details.
        workers: ``int``, optional
            Number of workers (default is ``os.cpu_count()``) to use
            for parallel computation.

            See `scipy.fft.rfft <https://docs.scipy.org/doc/scipy/
            reference/generated/scipy.fft.rfft.html>`_
            for more details.
        fft_output: ``bool``, optional
            - ``True`` to get same output as fft (default).
            - ``False`` to get truncated output (faster but :func:`.check`
              fails on forward - adjoint operators consistency).

    Returns:
        :class:`.LazyLinOp` real DFT

    Example:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> import scipy as sp
        >>> F = lz.wip.signal.rfft(32)
        >>> x = np.random.rand(32)
        >>> np.allclose(F @ x, sp.fft.fft(x, norm='ortho'))
        True
        >>> # easy inverse
        >>> F = lz.wip.signal.rfft(32, norm=None)
        >>> y = F @ x
        >>> x_ = F.inv() @ y # inverse works for any norm
        >>> np.allclose(x_, x)
        True

    .. seealso::
        `scipy.fft.rfft
        <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.rfft.html>`_,
        `scipy.fft.ifft
        <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.ifft.html>`_,
        :func:`.fft`
    """
    n_, N = _check_n(n, N)
    # L: size of output when real input
    nr = (n_ + 1) // 2 if (n_ & 1) else (n_ // 2) + 1

    def fft_rfft(x, axis, n, norm, workers):
        y = sp.fft.rfft(x.real, axis=axis, n=n, norm=norm, workers=workers)
        # assert nr == y.shape[0]
        if fft_output:
            # apply symmetry to build full fft output
            if n & 1:
                # n is odd
                fft_y = np.vstack((y, y[:0:-1].conj()))
            else:
                # n is even
                fft_y = np.vstack((y, y[nr-2:0:-1].conj()))
            # assert fft_y.shape[0] == n
            return fft_y
        else:
            return y

    def ifft_irfft(y, axis, n, norm, workers):
        # x = sp.fft.irfft(y[:nr], axis=axis, n=nr, norm=norm, workers=workers)
        # can't get irfft work properly
        if fft_output:
            x = sp.fft.ifft(y, axis=axis, n=n, norm=norm, workers=workers)
        else:
            x = sp.fft.irfft(y, axis=axis, n=n, norm=norm, workers=workers)
        return x

    return _fft(fft_rfft, ifft_irfft, N, n_, norm, workers, n_ if fft_output
                else nr, 'complex')


def _fft(sp_fft, sp_ifft, N, n: int = None,
         norm: str = None, workers: int = None, L: int = None,
         dtype: str = None):

    # n is input size
    # L is output size

    if norm not in _valid_norms:
        raise ValueError("norm must be either 'ortho'," +
                         " '1/n' or None.")
    sp_norm, sp_norm_inv = _scipy_norm(norm)

    def _matmat(x):
        # x is always 2d
        return sp_fft(x, axis=0, n=n,
                      norm=sp_norm, workers=workers)

    def _rmatmat(x):
        # x is always 2d
        y = sp_ifft(x, axis=0, n=n,
                    norm=sp_norm_inv, workers=workers)
        # len(y) must be N to match LazyLinOp shape
        if n == N:
            return y
        elif n < N:
            # crop case
            return np.pad(y, ((0, N - n), (0, 0)))
        else:
            # padded case
            # n > N
            return y[:N]

    L = LazyLinOpFFT(
        shape=(L, N),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x),
        dtype=dtype
    )
    L.norm = norm
    L.n = n
    return L


class LazyLinOpFFT(LazyLinOp):

    def inv(lz_fft):
        norm = lz_fft.norm
        n = lz_fft.n
        if norm == 'ortho':
            return lz_fft.H
        elif norm == '1/n':
            return n * lz_fft.H
        else:
            assert norm is None
            return 1/n * lz_fft.H


def _check_n(n, N):
    if isinstance(N, (int, float)):
        N = int(N)
    else:
        raise ValueError('N must be a number (int)')
    if n is None:
        n = N
    elif isinstance(n, (int, float)):
        n = int(n)
    else:
        raise ValueError('n must be a number (int)')
    return n, N


def _scipy_norm(lz_norm):
    # determine *fft, i*fft norm arguments
    # form lz norm argument
    if lz_norm is None:
        sp_norm = 'backward'
        sp_norm_inv = 'forward'
    elif lz_norm == '1/n':
        sp_norm = 'forward'
        sp_norm_inv = 'backward'
    else:  # lz_norm is 'ortho'
        assert lz_norm == 'ortho'
        sp_norm = sp_norm_inv = 'ortho'
    return sp_norm, sp_norm_inv
