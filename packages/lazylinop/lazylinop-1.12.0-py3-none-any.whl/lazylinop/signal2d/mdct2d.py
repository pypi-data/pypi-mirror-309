from lazylinop.basicops import kron
from lazylinop.signal import mdct


def mdct2d(in_shape: tuple, backend: str = 'scipy'):
    r"""
    Returns a :class:`.LazyLinOp` ``L`` for the 2D
    Modified Direct Cosine Transform (MDCT) of a 2D signal of
    shape ``in_shape=(M, N)`` (provided in flattened version).

    Shape of ``L`` is $(PQ,~MN)$ with $P=M/2$ and $Q=N/2$.

    :octicon:`alert-fill;1em;sd-text-danger` $M$ and $N$ must be
    multiples of $4$.

    After applying the operator as ``y = L @ flatten(X)``, a 2D
    output can be obtained via ``unflatten(y, out_shape)``
    with ``out_shape = (P / 2, Q / 2)``.

    ``L`` is *not* orthogonal (as it is rectangular with fewer
    rows than columns, it is not left invertible) but it is *right*-invertible
    and real-valued, with ``L @ L.T = L @ L.H = Id``.
    Thus, ``L.T`` can be used as a right-inverse.

    Args:
        in_shape: ``tuple``
            Shape of the 2d input array $(M,~N)$.

        backend: str, optional
            - ``'scipy'`` (default) uses ``scipy.fft.dct`` encapsulation
              for the underlying computation of the DCT.
            - ``'lazylinop'`` uses pre-built Lazylinop operators
              (Lazylinop :func:`.fft`, :func:`eye`, :func:`.vstack` etc.)
              to build the pipeline that will compute the MDCT.

    Returns:
        :class:`.LazyLinOp`

    Example:
        >>> from lazylinop.signal2d import mdct2d, flatten
        >>> import numpy as np
        >>> X = np.random.randn(32, 32)
        >>> L = mdct2d(X.shape)
        >>> Y = L @ flatten(X)
        >>> Y.shape[0] == (32 // 2) ** 2
        True
        >>> X_ = L.T @ Y
        >>> X_.shape[0] == 32 ** 2
        True

    References:
        - [1] Xuancheng Shao, Steven G. Johnson, Type-IV DCT, DST, and MDCT
          algorithms with reduced numbers of arithmetic operations,
          Signal Processing, Volume 88, Issue 6, 2008, Pages 1313-1326,
          ISSN 0165-1684, https://doi.org/10.1016/j.sigpro.2007.11.024.

    .. seealso::
        - `MDCT (Wikipedia) <https://en.wikipedia.org/wiki/
          Modified_discrete_cosine_transform>`_,
        - `Type-IV DCT, DST, and MDCT algorithms with reduced
          numbers of arithmetic operations <https://www.sciencedirect.com/
          science/article/pii/S0165168407003829?via%3Dihub>`_,
        - `SMAGT/MDCT <https://github.com/smagt/mdct>`_,
        - `MDCT.jl <https://github.com/stevengj/
          MDCT.jl/blob/master/src/MDCT.jl>`_,
        - `Nils Werner <https://github.com/nils-werner/mdct/blob/
          master/mdct/fast/transforms.py>`_,
        - :func:`lazylinop.signal.mdct`.
    """

    # Use mdct and kron lazy linear operators to write mdct2d.
    # Kronecker product trick: A @ X @ B^T = kron(A, B) @ vec(X).
    return kron(mdct(in_shape[0], backend),
                mdct(in_shape[1], backend))
