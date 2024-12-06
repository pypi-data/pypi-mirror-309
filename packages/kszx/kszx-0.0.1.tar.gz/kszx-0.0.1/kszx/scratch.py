

# FIXME from kszpipe
def estimate_power_spectrum(self, grid, kbin_delim, use_dc=False, use_nyquist=True):
    """
    Estimates auto power spectrum of Fourier-space grid in k-bins.
    Returns (binned_ps, bin_counts), 1-d arrays of length nbins.

    The 'kbin_delim' argument should be an array of length (nbins+1).
    The k-bins for power spectrum estimation are defined by:

           kbin_delim[0] <= k < kbin_delim[1]
              ...
           kbin_delim[nbins-1] <= k < kbin_delim[nbins]
   
    If use_dc=False, then the k=0 mode will not be used.
    If use_nyquist=False, then "Nyquist" modes will not be used.
    """
        
    kbin_delim = np.asarray(kbin_delim, dtype=float)

    assert self.is_fourier_space(grid)
    assert misc_utils.is_sorted(kbin_delim)
    assert kbin_delim[0] >= 0.0
    
    binned_ps, bin_counts = _box_utils.estimate_power_spectrum(grid, self.npix, self.boxsize, kbin_delim, use_dc, use_nyquist)
    return binned_ps, bin_counts


# FIXME from kszpipe
def estimate_power_spectra(self, grids, kbin_delim, faxis, use_dc=False, use_nyquist=True):
    """
    Estimate auto and cross power spectra of multiple Fourier-space grids.

    Returns (binned_ps, bin_counts), where 'binned_ps' has shape (nbins, ngrids, ngrids),
    and 'bin_counts' is a 1-d array of length nbins.

    The 'grids' argument represents a length-ngrids array of Fourier-space grids. The 'faxis'
    argument indicates which axis (usually the first or last) of the 'grids' array is the
    grid index 0 <= i < ngrids.

    The 'kbin_delim' argument should be an array of length (nbins+1).
    The k-bins for power spectrum estimation are defined by:

           kbin_delim[0] <= k < kbin_delim[1]
              ...
           kbin_delim[nbins-1] <= k < kbin_delim[nbins]

    If use_dc=False, then the k=0 mode will not be used.
    If use_nyquist=False, then "Nyquist" modes will not be used.
    """

    # Allows syntax Box.estimate_power_spectra([g1,g2], ..., faxis=0)
    grids = np.asarray(grids)
        
    if (grids.ndim != self.ndim + 1):
        raise RuntimeError("Box.estimate_power_spectra(): expected 'grids' array to have one higher dimension than Box array."
                           + " Maybe you meant to call estimate_power_spectrum() instead of estimate_power_spectra()?")

    assert 0 <= faxis < self.ndim
    grid_shape = grids.shape[:faxis] + grids.shape[(faxis+1):]
    
    if (grid_shape != self.fshape) or (grids.dtype != complex):
        raise RuntimeError(f"Box.estimate_power_spectra(): bad 'grids' shape/dtype (shape={grids.shape}, dtype={grids.dtype}, faxis={faxis})")

    kbin_delim = np.asarray(kbin_delim, dtype=float)
    assert misc_utils.is_sorted(kbin_delim)
    assert kbin_delim[0] >= 0.0
    
    binned_ps, bin_counts = _box_utils.estimate_power_spectra(grids, self.npix, self.boxsize, kbin_delim, faxis, use_dc, use_nyquist)
    return binned_ps, bin_counts


####################################################################################################


def multiply_rfunc(box, arr, f, dest=None):
    pass


def multiply_rhat(box, arr, i, dest=None, eps=1.0e-7):
    pass


def multiply_kfunc(box, arr, f, dest=None):
    """Applies function f(k) to Fourier-space map 'arr', where k = |\vec k| is a scalar wavenumber.

    The 'box' argument is an instance of class kszx.Box.
    The 'arr' argument is a numpy array with shape=box.fourier_space_shape and dtype=complex.
    The 'f' argument can be any callable object k -> f(k), where input/output arrays are multidimensional.

    FIXME arguments for kmin/kmax
    """
    pass


def multiply_khat(box, arr, i, dest=None):
    pass


def apply_partial_derivative(box, arr, d, dest=None):
    """
    Applies partial derivative (\partial / \partial x^d) in place to Fourier-space grid.
    Note that "Nyquist" modes will be zeroed, due to the k/-k ambiguity.
    """

    # FIXME kszpipe code starts here.
    # FIXME here and elsewhere, rename d -> axis.
    
    assert self.is_fourier_space(grid)
    assert 0 <= d < self.ndim
    grid *= (1j * self.get_k_component(d, zero_nyquist=True))


def apply_laplacian(box, arr, dest=None):
    pass


def apply_inverse_laplacian(box, arr, dest=None):
    """
    Applies inverse Laplacian (-1/k^2) in place to Fourier-space grid.
    Note that the k=0 mode will be zeroed, for lack of any better alternative.
    """
    
    # FIXME kszpipe code starts here.
    assert self.is_fourier_space(grid)
    grid /= self.get_k2(multiplier=-1.0, regulate=True)
    grid[(0,)*self.ndim] = 0.0  # Set k=0 to zero


def set_zero_above_kmax(self, grid, kmax):
    """Zeroes modes of Fourier-space grid with (k > kmax)."""
    assert self.is_fourier_space(grid)
    grid *= (self.get_k2() <= kmax**2)
        
    
def project_real(self, grid, *, multiplier=1.0):
    """
    Imposes reality condition f(k) = f(-k)^* on Fourier-space grid.
    The 'multiplier' argument is a hack for convenience in simulate_white_noise().
    """
        
    assert self.is_fourier_space(grid)

    self._project_real(grid[...,0], multiplier)
    if self.npix[-1] % 2 == 0:
        self._project_real(grid[...,-1], multiplier)
        

def _project_real(arr, multiplier):
    """Helper for non-static method project_real()."""
    arr *= (0.5 * multiplier)
    arr += _box_utils.reverse_array(arr).conj()



####################################################################################################


def simulate_gaussian_field(box, pk, kmax=None, zero_dc=False, dest=None):
    """Simulates a Gaussian Fourier-space field with specified power spectrum P(k).

    The 'box' argument is an instance of class kszx.Box.
    The 'pk' argument can be any callable object k -> P(k), where input/output arrays are multidimensional.
    If the 'kmax' argument is specified, then the output array will be zeroed for k > kmax.
    If the 'zero_dc' flag is specified, then 

    Note that the output array is a Fourier-space map (shape box.fourier_space_shape and dtype=complex).
    If a real-space map is preferred, then call fft_c2r() on the output array.

    Reminder: Fourier convention for simulated field is

       <f(k) f(-k')> = (box volume) P(k) delta_{kk'}  [ morally P(k) (2pi)^n delta^n(k-k') ]

    With this convention, calling fft_c2r() on the output gives a real-space map with the correct variance.
    """

    assert isinstance(box, Box)
    assert callable(pk)

    # FIXME kszpipe code starts here (note that pk is a scalar in this code)

    rms = np.sqrt(0.5 * pk * self.box_volume) if normalize else np.sqrt(0.5 * pk)
    ret = np.zeros(self.nk, dtype=complex)        
    ret.real = np.random.normal(size=self.nk, scale=rms)
    ret.imag = np.random.normal(size=self.nk, scale=rms)
    
    if project_real:
        self.project_real(ret, multiplier = np.sqrt(2.))
        
    if not simulate_dc:
        ret[(0,)*self.ndim] = 0.0
