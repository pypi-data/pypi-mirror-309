class PyBlockDim:
    """
    A class representing a dimension block. This is immutable. 
    
    :param width: a nonzero 32-bit integer
    :param height: a nonzero 32-bit integer
    :param depth: a nonzero 32-bit integer
    """

    def __init__(width: int, height: int, depth: int) -> PyBlockDim: ...

    def width(self) -> int:
        """
        Returns the width of the BlockDim
        """
    def height(self) -> int:
        """
        Returns the height of the BlockDim
        """
    def depth(self) -> int:
        """
        Returns the depth of the BlockDim
        """

def block_height_mip0(height: int) -> int:
    """
    Calculates the block height parameter to use for the first mip level if no block height is specified.
    
    :param height: image height in pixels for uncompressed formats (i.e. R8G8B8A8), or the height divided by the block dimensions (rounding up)
    """

def mip_block_height(mip_height: int, block_height_mip0: int) -> int: 
    """
    Calculates the block height parameter for the given mip level.
    
    :param mip_height: the mip's height in blocks
    :param block_height_mip0: the block height parameter for the first mip level
    
    See :func:`rust.block_height_mip0()`
    """

def swizzled_surface_size(width: int, height: int, depth: int, block_dim: PyBlockDim, block_height_mip0: int, bytes_per_pixel: int, mipmap_count: int, layer_count: int) -> int:
    """
    Calculates the size in bytes for the tiled data for the given surface.
    
    :param width: surface width in pixels
    :param height: surface height in pixels
    :param depth: surface depth in pixels
    :param block_dim: block dimensions
    :param block_height_mip0: see function block_height_mip0
    :param bytes_per_pixel: number of bytes in each pixel
    :param mipmap_count: number of mipmap levels
    :param layer_count: number of layers
    """

def deswizzle_block_linear(width: int, height: int, depth: int, source: bytes, block_height: int, bytes_per_pixel: int) -> bytes:
    """
    Untiles the blocks from source using block linear format.
    
    :param width: The width of the surface in blocks
    :param height: The height of the surface in blocks
    :param depth: The depth of the surface in blocks
    :param source: The raw data for the surface
    :param block_height: The block height (1,2,4,8,16,32)
    :param bytes_per_pixel: Number of bytes per pixel

    :returns: The deswizzled surface as bytes
    """