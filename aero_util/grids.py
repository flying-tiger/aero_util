import numpy as np
import xarray as xr
from itertools import chain

#-----------------------------------------------------------------------
# Helper Functions
#-----------------------------------------------------------------------
def _load_blocks(f, nblock):
    ''' Read Plot3D block data from file handle '''

    # Read header
    block_sizes = []
    for _ in range(nblock):
        words = next(f).strip().split()
        block_sizes.append(tuple(map(int, words)))

    # Set names that will used in xarray datasets
    ndims = len(block_sizes[0])
    coord_names = ('i', 'j', 'k')[:ndims]
    data_names  = ('x', 'y', 'z')[:ndims]

    # Parse coordinate data
    blocks = []
    words = chain.from_iterable(map(str.split, f))
    for size in block_sizes:
        coords = {n:range(s) for n,s in zip(coord_names, size)}
        nvals  = int(np.product(size))
        data   = {}
        for name in data_names:
            vals = np.fromiter(words, float, nvals)
            vals = np.reshape(vals, size, order='F')
            data[name] = (coord_names, vals)
        blocks.append(xr.Dataset(data, coords=coords))

    return blocks


#-----------------------------------------------------------------------
# Public API
#-----------------------------------------------------------------------
def load(filename):
    ''' Load block-structured grid from ASCII Plot3D file (2D or 3D) '''

    with open(filename) as f:
        line = next(f).strip().split()
        if len(line) == 1:
            # If first line is a single integer, it's a block count and
            # we have a multiblock grid. Proceed with read of all blocks.
            return _load_blocks(f, int(line[0]))

    # If first line is multiple integers, its a single block grid.
    # Reopen file to reset the iterator and read the block.
    with open(filename) as f:
        return _load_blocks(f, 1)



