
def randomize_array(arr, *, lo=-1.0, hi=1.0, rng=np.random.default_rng()):
    if arr.dtype == float:
        arr[:] = rng.uniform(lo, hi, arr.shape)
    elif arr.dtype == complex:
        arr.real = rng.uniform(lo, hi, arr.shape)
        arr.imag = rng.uniform(lo, hi, arr.shape)
    else:
        raise RuntimeError('dtype must be real or complex')

    
def random_array(dtype, *, shape=None, lo=-1.0, hi=1.0, pad=True, rng=np.random.default_rng()):
    if shape is None:
        shape = random_shape(rng=rng)
            
    if not pad:
        ret = np.empty(shape, dtype=dtype)
    else:
        # FIXME should sometimes make last axis non-contiguous
        shape = np.asarray(shape, dtype=int)
        new_shape = shape + rng.integers(0, 3, size=len(shape))
        ret = np.empty(new_shape, dtype=dtype)

        for d in range(len(shape)):
            if shape[d] < ret.shape[d]:
                ret = np.take(ret, np.arange(shape[d]), axis=d)
                
    assert np.all(np.asarray(shape) == np.asarray(ret.shape))
    randomize_array(ret, lo=lo, hi=hi, rng=rng)
    
    return ret

