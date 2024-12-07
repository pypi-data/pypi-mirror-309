import numpy as np
from lazylinop.basicops import block_diag, eye, kron, padder, vstack
from lazylinop.signal import dwt
from lazylinop.signal.utils import chunk
import sys
sys.setrecursionlimit(100000)


def dwt2d(in_shape: tuple, wavelet: str = 'haar',
          mode: str = 'zero', level: int = None,
          backend: str = 'pywavelets'):
    """
    Returns a :class:`.LazyLinOp` ``L`` for the 2D
    Discrete-Wavelet-Transform (DWT) a 2D signal of shape
    ``in_shape = (M, N)`` (provided in flattened version).

    ``L @ x`` will return a 1d NumPy array as the concatenation
    of the DWT coefficients in the form
    ``[cAn, cHn, cVn, cDn, ..., cH1, cV1, cD1]``
    where ``n`` is the decomposition level.

    - ``cAi`` are the approximation coefficients for level ``i``.
    - ``cHi`` are the horizontal coefficients for level ``i``.
    - ``cVi`` are the vertical coefficients for level ``i``.
    - ``cDi`` are the detail coefficients for level ``i``.
    ``cAi``, ``cHi``, ``cVi`` and ``cDi`` matrices have been flattened.

    Shape of ``L`` is $(P,~MN)$ where $P>=MN$.
    The value of $P$ depends on the ``mode``.
    In general, ``L`` is not orthogonal.

    Args:
        in_shape: ``tuple``
            Shape of the 2d input array $(M,~N)$.
        wavelet: ``str`` or tuple of ``(np.ndarray, np.ndarray)``, optional

            - If a ``str`` is provided, the wavelet name from
              `Pywavelets library <https://pywavelets.readthedocs.io/
              en/latest/regression/wavelet.html#
              wavelet-families-and-builtin-wavelets-names>`_
            - If a tuple of two ``np.ndarray`` is provided, the quadrature
              mirror filters of the wavelet.
        mode: ``str``, optional

            - ``'periodic'`` treat image as periodic image.
            - ``'symmetric'`` use mirroring to pad the signal.
            - ``'zero'`` use zero-padding (default).
        level: ``int``, optional
            If level is None compute full decomposition (default).
        backend: ``str``, optional
            ``'pywavelets'`` (default) or ``'lazylinop'`` for
            the underlying computation of the DWT.

    Returns:
        :class:`.LazyLinOp`

    Examples:
        >>> from lazylinop.signal2d import dwt2d, flatten
        >>> import numpy as np
        >>> import pywt
        >>> X = np.array([[1., 2.], [3., 4.]])
        >>> L = dwt2d(X.shape, wavelet='db1', level=1)
        >>> y = L @ flatten(X)
        >>> cA, (cH, cV, cD) = pywt.wavedec2(X, wavelet='db1', level=1)
        >>> z = np.concatenate([cA, cH, cV, cD], axis=1)
        >>> np.allclose(y, z)
        True

    .. seealso::
        - `Pywavelets module <https://pywavelets.readthedocs.io/en/
          latest/ref/2d-dwt-and-idwt.html#ref-dwt2>`_,
        - `Wavelets <https://pywavelets.readthedocs.io/en/latest/
          regression/wavelet.html>`_,
        - `Extension modes <https://pywavelets.readthedocs.io/en/
          latest/ref/signal-extension-modes.html>`_,
        - :func:`lazylinop.signal.dwt`.
    """
    if type(in_shape) is not tuple:
        raise Exception("in_shape expects tuple (M, N).")
    if len(in_shape) != 2:
        raise Exception("in_shape expects tuple (M, N).")
    if level is not None and level < 0:
        raise ValueError("Decomposition level must be >= 0.")
    if level is not None and level == 0:
        return eye(in_shape[0] * in_shape[1], in_shape[0] * in_shape[1], k=0)
    if backend != 'pywavelets' and backend != 'lazylinop':
        raise ValueError("backend must be either" +
                         " 'pywavelets' or 'lazylinop'.")

    found_pywt = False
    try:
        import pywt
        found_pywt = True
    except ModuleNotFoundError:
        pass

    if backend == "pywavelets" and not found_pywt:
        from warnings import warn
        warn("PyWavelets is not installed,"
             + " switch backend to 'lazylinop'.")
        backend = 'lazylinop'

    if backend == 'pywavelets' and mode != 'zero':
        str1 = "backend 'pywavelets' works only for mode='zero'."
        str2 = "Others modes are work-in-progress."
        raise ValueError(str1 + '\n' + str2)

    filters, pwavelet = None, None
    if not isinstance(wavelet, str):
        try:
            filters = tuple(wavelet)
            assert len(filters) == 2
            assert (
                isinstance(filters[0], np.ndarray) and
                isinstance(filters[1], np.ndarray)
            )
        except Exception:
            raise ValueError("'wavelet' argument must be a string" +
                             " or a tuple of two numpy arrays.")
        if found_pywt:
            pwavelet = pywt.Wavelet(
                "user_provided",
                [filters[0], filters[1], filters[0][::-1], filters[1][::-1]]
            )
    else:
        if not found_pywt:
            raise Exception("pywavelets module is required" +
                            " if 'wavelet' is a 'str')")
        pwavelet = pywt.Wavelet(wavelet)
        filters = (
            np.asarray(pwavelet.dec_lo),
            np.asarray(pwavelet.dec_hi)
        )
    W = pwavelet.dec_len

    # Shape of the 2d array
    M, N = in_shape[0], in_shape[1]
    # Shape of the 1d input
    MN = in_shape[0] * in_shape[1]
    # Stop decomposition when the signal becomes
    # shorter than the filter length
    K = min(int(np.log2(M / (W - 1))), int(np.log2(N / (W - 1))))
    if level is not None and level > K:
        raise Exception("Decomposition level is greater than" +
                        " the maximum decomposition level.")
    D = K if level is None else min(K, level)
    if D == 0:
        # Nothing to decompose, return identity matrix
        return eye(MN, MN, k=0)

    L = None
    for _ in range(D):
        # Use dwt and kron lazy linear operators to write dwt2d
        # Kronecker product trick: A @ X @ B^T = kron(A, B) @ vec(X)
        K = kron(
            dwt(M, wavelet=wavelet, mode=mode, level=1, backend=backend),
            dwt(N, wavelet=wavelet, mode=mode, level=1, backend=backend)
        )
        # Extract four sub-images (use slices operator)
        # ---------------------
        # | LL (cA) | LH (cH) |
        # ---------------------
        # | HL (cV) | HH (cD) |
        # ---------------------
        M = (M + W - 1) // 2
        N = (N + W - 1) // 2
        # Slices to extract detail, vertical and horizontal
        # coefficients and fill the following list of
        # coefficients [cAn, cHn, cVn, cDn, ..., cH1, cV1, cD1]
        # Slices to extract sub-image LL
        V = chunk(K.shape[0], N, 2 * N, start=0, stop=2 * N * M)
        # Slices to extract sub-image LH
        V = vstack((V, chunk(K.shape[0], N, 2 * N,
                             start=2 * N * M, stop=4 * N * M)))
        # Slices to extract sub-image HL
        V = vstack((V, chunk(K.shape[0], N, 2 * N,
                             start=N, stop=2 * N * M + N)))
        # Slices to extract sub-image HH
        V = vstack((V, chunk(K.shape[0], N, 2 * N, start=2 * N * M + N)))
        if L is None:
            # First level of decomposition
            L = V @ K
        else:
            # Apply low and high-pass filters + decimation only to LL
            # Because of lazy linear operator V, LL always comes first
            L = block_diag(*[V @ K,
                             eye(L.shape[0] - K.shape[1],
                                 L.shape[0] - K.shape[1])]) @ L
    return L


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
