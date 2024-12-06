import kszpipe
import numpy as np


def test_k():
    """Is there any rescuing this disaster??"""
    
    print(f'test_k(): start')
    
    for iouter in range(100):
        box = helpers.random_box()
        exponent = min(np.random.uniform(-2,3), 2)
        regulate = np.random.uniform() < 0.3
        ret = box.get_k(exponent, regulate)

        kmin = min(2*np.pi/box.boxsize) if (regulate or exponent < 0) else 0.
        k2 = [ box.get_k_component(ax, zero_nyquist=False, one_dimensional=True)**2 for ax in range(box.ndim) ]
        epsilon = 0.0
        
        for iinner in range(100):
            ix = [ np.random.randint(0,n) for n in box.nk ]
            if iinner == 0:
                ix = [ 0 for n in box.nk ]

            lhs = ret[np.array(ix)]
            print(f'{ret.shape=} {ix=} {lhs.shape=}')
            rhs = sum(k2[i][j] for i,j in enumerate(ix))
            rhs = max(rhs, kmin)
            rhs = rhs**(exponent/2.)
            print(f'{lhs.shape=} {rhs.shape=}')

            num = np.abs(lhs-rhs) 
            den = (lhs+rhs) if (lhs+rhs > 0) else 1.
            epsilon += (num/den)

        print(f'{epsilon=}')
        
    print(f'test_k(): pass')


####################################################################################################


def test_kmax():
    for iouter in range(100):
        box = kszpipe.Box.make_random()
        if np.all(box.npix == 1):
            continue
        
        kmax = [ np.max(box.get_k_component(d, zero_nyquist=False)) for d in range(box.ndim) ]
        kmax = np.dot(kmax,kmax)**0.5
        eps = np.abs(box.kmax - kmax) / kmax
        assert eps < 1.0e-14
        


####################################################################################################


def make_sinusoid(box, coeff, ivec):
    nd = box.ndim
    assert ivec.shape == (nd,)
    assert ivec.dtype == int

    grid = np.full(box.npix, coeff, dtype=complex)

    for d in range(nd):
        n = box.npix[d]
        u = np.exp((2j*np.pi * ivec[d] / float(n)) * np.arange(n))
        shape = (1,)*d + (n,) + (1,)*(nd-d-1)
        grid *= u.reshape(shape)

    return grid.real


def test_apply_partial_derivative():
    for iouter in range(1000):
        ndim = np.random.randint(1, 4)
        npix = np.random.randint(4, 10, ndim)
        box = kszpipe.Box.make_random(npix)
        coeff = np.random.normal() + np.random.normal()*1j
        ivec = np.random.randint(0, npix)
        d = np.random.randint(0, ndim)
        
        grid = make_sinusoid(box, coeff, ivec)
        grid = box.fft(grid)
        box.apply_partial_derivative(grid, d)
        grid = box.fft(grid)

        n = npix[d]
        i = ivec[d]
        kf = 2*np.pi / box.boxsize[d]
        
        if 2*i < n:
            k = kf * i
        elif 2*i == n:
            k = 0.
        else:
            k = kf * (i-n)

        grid2 = make_sinusoid(box, 1j * k * coeff, ivec)
        eps = np.max(np.abs(grid - grid2)) / kf
        assert eps < 1.0e-13


def test_apply_inverse_laplacian():
    for iouter in range(1000):
        ndim = np.random.randint(1, 4)
        npix = np.random.randint(4, 10, ndim)
        box = kszpipe.Box.make_random(npix)
        coeff = np.random.normal() + np.random.normal()*1j
        ivec = np.random.randint(0, npix)
        d = np.random.randint(0, ndim)

        grid = make_sinusoid(box, coeff, ivec)
        grid = box.fft(grid)
        box.apply_inverse_laplacian(grid)
        grid = box.fft(grid)

        k2 = 0.0
        for d in range(ndim):
            n = npix[d]
            i = ivec[d]
            j = i if (2*i <= n) else (i-n)
            k2 += ((2*np.pi / box.boxsize[d]) * j)**2

        w = (-1.0/k2) if (k2 > 0.0) else 0.0
        grid2 = make_sinusoid(box, w*coeff, ivec)
        
        eps = np.max(np.abs(grid - grid2)) / np.max(box.boxsize)**2
        assert eps < 1.0e-15             
        
        
####################################################################################################


def reverse_array_slow(arr):
    for d in range(arr.ndim):
        n = arr.shape[d]
        ix = [ 0 ] + list(range(n-1,0,-1))
        arr = np.take(arr, ix, axis=d)
    return arr
    

def test_reverse_array():
    for iouter in range(100):
        for dtype in [ float, complex ]:
            arr = kszpipe.misc_utils.random_array(dtype)
            revslow = reverse_array_slow(arr)
            revfast = kszpipe._box_utils.reverse_array(arr)
            assert np.all(revslow == revfast)


####################################################################################################


def rotate_array(arr, roffsets):
    roffsets = np.asarray(roffsets, dtype=int)
    assert np.all(roffsets.shape == (arr.ndim,))

    for d in range(arr.ndim):
        r = roffsets[d]
        n = arr.shape[d]
        assert 0 <= r < n

        s = np.concatenate((np.arange(r,n), np.arange(0,r)))
        arr = np.take(arr, s, axis=d)

    return arr



####################################################################################################
#
# In the following tests:
#   Let P = project_real() operation
#   Let F = fft() in r2c direction
#   Let F^T = fft() in c2r direction
#
# Test 1: F^T F = 1
# Test 2: P^2 = P
# Test 3: PF = F
# Test 4: F F^T P = P
# Test 5: F and F^T are transposes



def test_fft2():
    """Test 2: P^2 = P."""

    for iouter in range(100):
        box = kszpipe.Box.make_random()
        Px = box.simulate_white_noise(fourier=True, normalize=False, project_real=True)
        PPx = np.copy(Px)
        box.project_real(PPx)

        eps = np.max(np.abs(Px - PPx))
        assert eps < 1.0e-13


def test_fft3():
    """Test 3: PF = F."""

    for iouter in range(100):
        box = kszpipe.Box.make_random()
        x = box.simulate_white_noise(fourier=False, normalize=False)
        Fx = box.fft(x)
        
        PFx = np.copy(Fx)
        box.project_real(PFx)

        eps = np.max(np.abs(Fx-PFx)) / np.max(np.abs(Fx))
        assert eps < 1.0e-13


def test_fft4():
    """Test 4: F F^T P = P."""

    for iouter in range(100):
        box = kszpipe.Box.make_random()
        Px = box.simulate_white_noise(fourier=True, normalize=False, project_real=True)
        FPx = box.fft(Px)
        FFPx = box.fft(FPx)

        eps = np.max(np.abs(Px - FFPx))
        assert eps < 1.0e-13


####################################################################################################


def test_white_noise():
    if False:
        print(f'Note: test_white_noise() is a little slow (~10 seconds) and currently disabled')
        return
        
    for npix in [ [4,4], [4,5], [5,4], [5,5] ]:
        box = kszpipe.Box.make_random(npix=npix)
        pk = np.random.uniform(10.0, 100.0)

        acc_shape = box.fshape + (2,)
        acc = np.zeros(acc_shape)
        acc2 = np.zeros(acc_shape)
    
        for nmc in range(1,20001):
            grid_f = box.simulate_white_noise(fourier=True, pk=pk)
            grid_r = box.simulate_white_noise(fourier=False, pk=pk)
            grid_f2 = box.fft(grid_r)

            acc[...,0] += grid_f.real**2
            acc[...,1] += grid_f.imag**2
            acc2[...,0] += grid_f2.real**2
            acc2[...,1] += grid_f2.imag**2

        var = 0.5 * pk * box.box_volume
        eps = np.max(np.abs(acc-acc2)) / nmc / var
        print(f'test_white_noise: {box}, eps={eps}')
        assert eps < 0.2

        
def test_white_noise2():
    if False:
        print(f'Note: test_white_noise2() is a little slow (~10 seconds) and currently disabled')
        return

    for npix in [ [16,16], [16,15], [15,16], [15,15] ]:
        box = kszpipe.Box.make_random(npix=npix)
        pk = np.random.uniform(10.0, 100.0)
        nbins = 5
    
        kbin_delim = np.linspace(0.0, 1.01 * box.kmax, nbins+1)
        accum_ps = np.zeros(nbins)
    
        for nmc in range(1,10001):
            grid = box.simulate_white_noise(fourier=True, pk=pk)
            ps, counts = box.estimate_power_spectrum(grid, kbin_delim, use_dc=True, use_nyquist=True)
            assert np.sum(counts) == np.prod(box.npix)
            accum_ps += ps

        eps = np.max(np.abs(accum_ps/pk/nmc) - 1.0)
        print(f'test_white_noise2: {box}, eps={eps}')
        assert eps < 0.01


####################################################################################################

    
def test_box_filter():
    rng = np.random.default_rng()
    
    for iouter in range(100):
        box = kszpipe.Box.make_random()
        a = np.min(box.boxsize) * rng.uniform(-1.0, 1.0)
        b = rng.uniform(0, 2*np.pi)
        f = lambda k: np.sin(a*k + b)
        dc = rng.uniform() if (rng.uniform() > 0.5) else None
        bf = kszpipe.BoxFilter(box, f, dc=dc)

        grid = box.simulate_white_noise(fourier=True, normalize=False)
        
        fgrid = np.copy(grid)
        bf.apply(fgrid)

        eps = 0.0
        
        for i in generate_indices(box.fshape):
            k = np.array(i, dtype=float)
            k = np.minimum(k, box.npix - k)
            k *= (2*np.pi) / box.boxsize
            k = np.dot(k,k)**0.5
            fk = f(k) if ((k > 0) or (dc is None)) else dc
            fg2 = fk * grid[i]
            eps = max(eps, np.abs(fg2 - fgrid[i]))

        assert eps < 1.0e-13
