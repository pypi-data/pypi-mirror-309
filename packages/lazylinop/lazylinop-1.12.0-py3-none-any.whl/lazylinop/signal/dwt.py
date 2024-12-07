import numpy as np
from lazylinop import LazyLinOp
import sys
from lazylinop.basicops import block_diag, eye, vstack
from lazylinop.wip.signal import ds_mconv
from lazylinop.basicops import padder, slicer
from lazylinop.signal import convolve
from lazylinop.signal.utils import decimate
sys.setrecursionlimit(100000)


def dwt(N: int, wavelet: str = 'haar',
        mode: str = 'zero', level: int = None,
        backend: str = 'pywavelets'):
    """
    Returns a :class:`.LazyLinOp` ``L`` for the
    Discrete Wavelet Transform (DWT).
    ``L @ x`` will return a 1D numpy array as the concatenation
    of the DWT coefficients in the form
    ``[cAₙ, cDₙ, cDₙ₋₁, …, cD₂, cD₁]``,
    where ``n`` is the decomposition level,
    ``cAₙ`` is the approximation coefficients for level ``n``
    and ``cDᵢ`` is the detail coefficients at decomposition level ``i``.

    Shape of ``L`` is $(M,~N)$ where $M$ depends on the wavelet,
    input size and decomposition level. In general, ``L`` is not orthogonal.

    Args:
        N: ``int``
            Size of the input array.
        wavelet: ``str`` or tuple of ``(np.ndarray, np.ndarray)``, optional

            - If a ``str`` is provided, the wavelet name from
              `Pywavelets library <https://pywavelets.readthedocs.io/en/latest/
              regression/wavelet.html#wavelet-families-and-builtin-wavelets-names>`_
            - If a tuple of two ``np.ndarray`` is provided, the low and
              high-pass filters used to define the wavelet.
              :octicon:`megaphone;1em;sd-text-danger` The ``dwt()`` function
              does not test Quadrature-Mirror-Filters of the custom wavelet.
        mode: ``str``, optional

            - 'antisymmetric', signal is extended by mirroring and
              multiplying elements by minus one.
            - 'periodic', signal is treated as periodic signal.
              Only works with ``backend='lazylinop'``.
            - 'reflect', signal is extended by reflecting elements.
            - 'symmetric', use mirroring to pad the signal.
              Only works with ``backend='lazylinop'``.
            - 'zero', signal is padded with zeros (default).
        level: ``int``, optional
            Decomposition level, by default (None) the maximum level is used
        backend: ``str``, optional
            'pywavelets' (default) or 'pyfaust' for the underlying
            computation of the DWT.

    Returns:
        :class:`.LazyLinOp` DWT.

    Examples:
        >>> from lazylinop.signal import dwt
        >>> import numpy as np
        >>> import pywt
        >>> N = 8
        >>> x = np.arange(1, N + 1, 1)
        >>> L = dwt(N, mode='periodic', level=1, backend='lazylinop')
        >>> y = L @ x
        >>> z = pywt.wavedec(x, wavelet='haar', mode='periodic', level=1)
        >>> np.allclose(y, np.concatenate(z))
        True

    .. seealso::
        - `Pywavelets module <https://pywavelets.readthedocs.io/en/
          latest/index.html>`_,
        - `Wavelets <https://pywavelets.readthedocs.io/en/latest/
          regression/wavelet.html>`_,
        - `Extension modes <https://pywavelets.readthedocs.io/en/
          latest/ref/signal-extension-modes.html>`_,
        - `Efficient Adjoint Computation for Wavelet and Convolution
          Operators <https://arxiv.org/pdf/1707.02018>`_.
    """

    if level is not None and level < 0:
        raise ValueError("Decomposition level must be >= 0.")
    if mode not in ['antisymmetric', 'reflect',
                    'periodic', 'symmetric', 'zero']:
        raise ValueError("mode is either 'antisymmetric', 'reflect',"
                         + " 'periodic', 'symmetric' or 'zero'.")
    if level is not None and level == 0:
        # Nothing to decompose, return identity matrix
        return eye(N, N)

    if backend not in ("pywavelets", "lazylinop"):
        raise ValueError("'backend' is either 'pywavelet' or 'lazylinop'")

    found_pywt = False
    try:
        import pywt
        found_pywt = True
    except ModuleNotFoundError:
        pass

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

    if backend == "pywavelets" and not found_pywt:
        from warnings import warn
        warn("PyWavelets is not installed,"
             + " switch backend to 'lazylinop'.")
        backend = 'lazylinop'

    if backend == 'pywavelets' and mode != 'zero':
        str1 = "backend 'pywavelets' works only for mode='zero'."
        str2 = "Others modes are work-in-progress."
        raise ValueError(str1 + '\n' + str2)

    if backend == 'pywavelets':

        # Name of the wavelet to use with rmatmat
        if 'rbio' in pwavelet.name:
            rwavelet = pywt.Wavelet('bior' + pwavelet.name[-3:])
        elif 'bior' in pwavelet.name:
            rwavelet = pywt.Wavelet('rbio' + pwavelet.name[-3:])
        else:
            rwavelet = pwavelet
        # Wavelet length
        W = pwavelet.dec_len

        # Compute length of the output (number of coefficients)
        tmp = N
        ncoeffs = 0
        for i in range(
                pywt.dwt_max_level(N, W) if level is None else level):
            # Number of details coefficients
            tmp = pywt.dwt_coeff_len(tmp, W, mode=mode)
            ncoeffs += tmp
        # Number of approximation coefficients
        ncoeffs += tmp

        # Get slices for further reconstruction (rmatmat).
        # Do it once and for all.
        # Of note, we have no idea about the batch size here.
        rslices = pywt.coeffs_to_array(
            pywt.wavedecn(
                np.full((N, 1), 1.0), wavelet=pwavelet,
                level=level, mode=mode, axes=(0, )
            ), axes=(0, )
        )[1]

        def _matmat(x):
            # Decomposition (return array from coefficients)
            # x is always 2d
            y = pywt.coeffs_to_array(
                pywt.wavedecn(
                    x, wavelet=pwavelet,
                    level=level, mode=mode, axes=(0, )
                ),
                axes=(0, )
            )[0]
            return y[:ncoeffs, :]

        def _rmatmat(x, rslices):
            # Reconstruction
            # x is always 2d
            # Size of the batch is not always the same.
            tmp = slice(rslices[0][1].start, x.shape[1], rslices[0][1].step)
            rslices[0] = (rslices[0][0], tmp)
            x_ = pywt.array_to_coeffs(x, rslices, output_format='wavedecn')
            y = pywt.waverecn(x_, wavelet=rwavelet, mode=mode, axes=(0, ))
            return y[:N, :]

        return LazyLinOp(
            shape=(ncoeffs, N),
            matmat=lambda x: _matmat(x),
            rmatmat=lambda x: _rmatmat(x, rslices)
        )

    elif backend == 'lazylinop':

        lfilter, hfilter = filters
        W = hfilter.shape[0]
        if W > N:
            # Nothing to decompose, return identity matrix
            return eye(N, N)

        boffset = (W % 4) == 0

        # Maximum decomposition level: stop decomposition when
        # the signal becomes shorter than the filter length
        K = int(np.log2(N / (W - 1)))
        if level is not None and level > K:
            raise ValueError("level is greater than the" +
                             " maximum decomposition level.")
        D = K if level is None else level

        if D == 0:
            # Nothing to decompose, return identity matrix
            return eye(N, N)

        # Loop over the decomposition level
        cx = N
        for i in range(D):
            # Boundary conditions
            npd = W - 2
            NN = cx + 2 * npd
            if mode == 'zero':
                NN += NN % 2
                B = eye(NN, cx, k=-npd)
            else:
                mx = NN % 2
                bn = npd
                an = npd + mx
                NN += mx
                B = padder(cx, (bn, an), mode=mode)
            # Low and high-pass filters + decimation
            # Decimation starts at offset_d
            offset_d = 1 - int(boffset)
            if 0:
                # Convolution low and high-pass filters + down-sampling
                GH = ds_mconv(NN, lfilter, hfilter,
                              mode='same', offset=offset_d, every=2) @ B
            else:
                # Convolution
                G = convolve(NN, lfilter, mode='same',
                             backend='scipy_convolve')
                H = convolve(NN, hfilter, mode='same',
                             backend='scipy_convolve')
                # Down-sampling
                DG = decimate(G.shape[0], 2, offset_d)
                DH = decimate(H.shape[0], 2, offset_d)
                # Vertical stack
                GH = vstack((DG @ G, DH @ H)) @ B
            # Extract approximation and details coefficients cA, cD
            cx = ((N if i == 0 else cx) + W - 1) // 2
            offset = (NN // 2 - cx) // 2 + int(boffset)
            # Slices to extract cA and cD
            V = slicer(GH.shape[0], [offset, offset + NN // 2],
                       [offset + cx, offset + NN // 2 + cx])
            if i == 0:
                # First level of decomposition
                Op = V @ GH
            else:
                # Apply low and high-pass filters + decimation only to cA
                # Because of lazy linear operator V, cA always comes first
                Op = block_diag(*[V @ GH,
                                  eye(Op.shape[0] - GH.shape[1],
                                      Op.shape[0] - GH.shape[1],
                                      k=0)
                                  ]
                                ) @ Op
        return Op
    else:
        raise ValueError("backend must be either 'pywavelets'"
                         + " or 'lazylinop'.")


# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
