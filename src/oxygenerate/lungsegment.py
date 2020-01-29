from skimage import measure, morphology, segmentation
import scipy
import scipy.ndimage as ndimage
import numpy as np

def generate_markers_np(npimage):
    # Creation of the internal Marker
    marker_internal = npimage < -400  # Lung Tissue threshold
    marker_internal = segmentation.clear_border(marker_internal)
    marker_internal_labels = measure.label(marker_internal)
    areas = [r.area for r in measure.regionprops(marker_internal_labels)]
    areas.sort()
    if len(areas) > 2:
        for region in measure.regionprops(marker_internal_labels):
            if region.area < areas[-2]:
                for coordinates in region.coords:
                    marker_internal_labels[coordinates[0], coordinates[1]] = 0

    marker_internal_labels = measure.label(marker_internal_labels)

    # Creation of the external Marker

    external_a = ndimage.binary_dilation(marker_internal_labels, iterations=20)
    external_b = ndimage.binary_dilation(marker_internal_labels, iterations=60)
    marker_external = external_b ^ external_a

    # Creation of the Watershed Marker matrix
    img_length = len(image[1])
    marker_watershed = np.zeros((img_length, img_length), dtype=np.float64)

    marker_watershed += marker_internal_labels * 255
    marker_watershed += marker_external * 128

    return marker_internal_labels, marker_watershed


# Function using watershed algorithm ro to lung segmentation
def lung_segment_np(npimage):
    # Creation of the markers:
    marker_internal, marker_watershed = generate_markers_np(npimage)

    # Creation of the Sobel-Gradient:
    sobel_filtered_dx = ndimage.sobel(npimage, 1)
    sobel_filtered_dy = ndimage.sobel(npimage, 0)
    sobel_gradient = np.hypot(sobel_filtered_dx, sobel_filtered_dy)

    # Watershed algorithm:
    watershed = morphology.watershed(sobel_gradient, marker_watershed)
    for i in range(npimage.shape[0]):
        for j in range(npimage.shape[1]):
            if watershed[i, j] == 128:
                watershed[i, j] = 0
    lung_centroids = [l.centroid for l in measure.regionprops(watershed)]
    labels = [label.label for label in measure.regionprops(watershed)]
    if lung_centroids[0][1] > 0.5 * len(npimage[1]) and labels[0] == 255:
        left_lung = watershed == 255  # marking left lung
        right_lung = watershed == 510  # marking right lung
    else:
        left_lung = watershed == 510
        right_lung = watershed == 255
    left_lung[left_lung != 0] = 1
    right_lung[right_lung != 0] = 2
    left_lung = left_lung * 5.0
    right_lung = right_lung * 17.0
    lungs = right_lung + left_lung

    return lungs, left_lung, right_lung


# a function to downsample the image stack to make the code run faster
def downsample_np(npimage, scan, new_spacing=[1, 1, 1]):
    # Determine current pixel spacing
    spacing = map(float, ([scan[0].SliceThickness] + scan[0].PixelSpacing))
    spacing = np.array(list(spacing))

    resize_factor = spacing / new_spacing
    new_real_shape = npimage.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / npimage.shape
    new_spacing = spacing / real_resize_factor

    npimage = scipy.ndimage.interpolation.zoom(npimage, real_resize_factor)

    return npimage, new_spacing