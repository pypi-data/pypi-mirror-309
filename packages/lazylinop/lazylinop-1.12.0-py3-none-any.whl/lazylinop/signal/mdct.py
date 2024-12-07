from lazylinop.basicops import eye
from lazylinop.basicops import hstack
from lazylinop.basicops import vstack
from lazylinop.basicops import anti_eye
from lazylinop.signal import dct
import numpy as np
import sys
sys.setrecursionlimit(100000)


def mdct(N, backend: str = 'scipy'):
    r"""
    Returns a :class:`.LazyLinOp` ``L`` for the
    Modified Direct Cosine Transform (MDCT).

    Shape of ``L`` is $(H,~N)$ with $H=N/2$.
    :octicon:`alert-fill;1em;sd-text-danger` $N$ must be multiple of $4$.

    ``X = L @ x`` yiels a vector ``X`` of size $H$ such that:

    .. math::

        \begin{equation}
        X_k=\frac{1}{\sqrt{H}}\sum_{n=0}^{N-1}x_n\cos\left(\frac{\pi}{H}\left(n+\frac{1}{2}+\frac{H}{2}\right)\left(k+\frac{1}{2}\right)\right)
        \end{equation}

    The function provides two backends: SciPy and Lazylinop for
    the underlying computation of DCT.

    The operator ``L`` is rectangular and is not left invertible.
    It is however right-invertible as ``L @ L.T``. Thus, ``L.T`` can be
    used as a right-inverse.

    ``y = L.T @ X`` yields a vector ``y`` of size $N$ such that:

    .. math::

        \begin{equation}
        y_n=\frac{1}{\sqrt{H}}\sum_{k=0}^{H-1}X_k\cos\left(\frac{\pi}{H}\left(n+\frac{1}{2}+\frac{H}{2}\right)\left(k+\frac{1}{2}\right)\right)
        \end{equation}

    Args:
        N: ``int``
            Size of the signal. ``N`` must be even.

        backend: str, optional
            - ``'scipy'`` (default) uses ``scipy.fft.dct`` encapsulation
              for the underlying computation of the DCT.
            - ``'lazylinop'`` uses pre-built Lazylinop operators
              (Lazylinop :func:`.fft`, :func:`eye`, :func:`.vstack` etc.)
              to build the pipeline that will compute the MDCT.

    Returns:
        :class:`.LazyLinOp`

    Example:
        >>> from lazylinop.signal import mdct
        >>> import numpy as np
        >>> x = np.random.randn(64)
        >>> L = mdct(64)
        >>> y = L @ x
        >>> y.shape[0] == 32
        True
        >>> x_ = L.T @ y
        >>> x_.shape[0] == 64
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
        - :func:`.dct`.
    """

    if (N % 2) != 0:
        raise Exception("N must be even.")
    if (N % 4) != 0:
        raise Exception("N/2 must be even.")

    H = N // 2
    Q = H // 2

    # Extract first sequence (see References [1]).
    V = -vstack(
        (
            anti_eye(Q, Q, k=0) @ eye(Q, N, k=H),
            eye(Q, N, k=3 * Q)
        )
    )
    # Compute the sum of the first half with the second one.
    H1 = hstack((eye(Q, Q, k=0), eye(Q, Q, k=0))) @ V
    # Extract second sequence (see References [1]).
    H2 = vstack(
        (
            eye(Q, N, k=0),
            -anti_eye(Q, Q, k=0) @ eye(Q, N, k=Q)
        )
    )
    # Compute the sum of the first half with the second one.
    H2 = hstack((eye(Q, Q, k=0), eye(Q, Q, k=0))) @ H2
    # Compute two DCT IV and subtract the two results (see References [1]).
    D = dct(H, 4, backend=backend)

    # return np.sqrt(H) * (D @ vstack((H1, H2)))
    return D @ vstack((H1, H2)) / np.sqrt(2.0)
