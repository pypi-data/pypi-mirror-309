from . import rust, version


def block_height_mip0(height: int) -> int:
    """
    Calculates the block height parameter to use for the first mip level if no block height is specified.
    
    :param height: image height in pixels for uncompressed formats (i.e. R8G8B8A8), or the height divided by the block dimensions (rounding up)
    """
    return rust.block_height_mip0(height)

def mip_block_height(mip_height: int, block_height_mip0: int) -> int:
    """
    Calculates the block height parameter for the given mip level.
    
    :param mip_height: the mip's height in blocks
    :param block_height_mip0: the block height parameter for the first mip level
    
    See :func:`block_height_mip0()`
    """
    return rust.mip_block_height(mip_height, block_height_mip0)

PyBlockDim = rust.PyBlockDim

def get_swizzled_surface_size(
        width: int, height: int, depth: int,
        block_dim: PyBlockDim, block_height_mip0: int,
        bpp: int, mipmap_count: int = 1, layer_count: int = 1
):
    """
    Calculates the size in bytes for the tiled data for the given surface.
    
    :param width: surface width in pixels
    :param height: surface height in pixels
    :param depth: surface depth in pixels
    :param block_dim: block dimensions
    :param block_height_mip0: see function block_height_mip0
    :param bytes_per_pixel: number of bytes in each pixel
    :param mipmap_count: number of mipmap levels
    :param layer_count: number of layers"""
    return rust.swizzled_surface_size(width, height, depth, block_dim, block_height_mip0, bpp, mipmap_count, layer_count)

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
    return rust.deswizzle_block_linear(width, height, depth, source, block_height, bytes_per_pixel)

__version__ = version.version
VERSION = version.version