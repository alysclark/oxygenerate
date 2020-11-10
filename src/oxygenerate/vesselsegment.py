from skimage import morphology

def centreline_extraction_3d(mask):
    out_skeletonise = morphology.skeletonize_3d(mask)
    return out_skeletonise