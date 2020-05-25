from PIL import ImageOps

from src.histolab.filters import image_filters_functional as F


class Compose(object):
    """Composes several filters together.

    Parameters
    ----------
    filters : list of Filters
        List of filters to compose
    """

    def __init__(self, filters):
        self.filters = filters

    def __call__(self, img):
        for f in self.filters:
            img = f(img)
        return img


class Invert(object):
    """Invert an image, i.e. take the complement of the correspondent array.

    Parameters
    ----------
    img : PIL.Image.Image
        Input image

    Returns
    -------
    PIL.Image.Image
        Inverted image
    """

    def __call__(self, img):
        return F.invert(img)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class RgbToGrayscale(object):
    """Convert an RGB image to a grayscale image.

    Parameters
    ----------
    img : PIL.Image.Image
         Input image

    Returns
    -------
    PIL.Image.Image
        Grayscale image
    """

    def __call__(self, img):
        return ImageOps.grayscale(img)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class RgbToHed(object):
    """Convert RGB channels to HED channels.

    image color space (RGB) is converted to Hematoxylin-Eosin-Diaminobenzidine space.

    Parameters
    ----------
    img : PIL.Image.Image
        Input image

    Returns
    -------
    PIL.Image.Image
        Image in HED space
    """

    def __call__(self, img):
        hed = F.rgb_to_hed(img)
        return hed

    def __repr__(self):
        return self.__class__.__name__ + "()"


class RgbToHsv(object):
    """Convert RGB channels to HSV channels.

    image color space (RGB) is converted to Hue - Saturation - Value (HSV) space.

    Parameters
    ----------
    img : PIL.Image.Image
         Input image

    Returns
    -------
    PIL.Image.Image
        Image in HED space
    """

    def __call__(self, img):
        hsv = F.rgb_to_hsv(img)
        return hsv

    def __repr__(self):
        return self.__class__.__name__ + "()"


class StretchContrast(object):
    """Increase image contrast.

    Th contrast in image is increased based on intensities in a specified range

    Parameters
    ----------
    img: PIL.Image.Image
         Input image
    low: int
         Range low value (0 to 255).
    high: int
          Range high value (0 to 255).

    Returns
    -------
    PIL.Image.Image
            Image with contrast enhanced.
    """

    def __call__(self, img, low, high):
        stretch_contrast = F.stretch_contrast(img, low, high)
        return stretch_contrast

    def __repr__(self):
        return self.__class__.__name__ + "()"


class HistogramEqualization(object):
    """Increase image contrast using histogram equalization.

    The input image (gray or RGB) is filterd using histogram equalization to increase
    contrast.

    Parameters
    ----------
    img : PIL.Image.Image
          Input image.
    nbins : iny. optional (default is 256)
          Number of histogram bins.

    Returns
    -------
    NumPy array (float or uint8) with contrast enhanced by histogram equalization.
    """

    def __call__(self, img, n_bins):
        hist_equ = F.histogram_equalization(img, n_bins)
        return hist_equ

    def __repr__(self):
        return self.__class__.__name__ + "()"


class AdaptiveEqualization(object):
    """Increase image contrast using adaptive equalization.

    Contrast in local region of input image (gray or RGB) is increased using
    adaptive equalization

    Parameters
    ----------
    img : PIL.Image.Image
           Input image (gray or RGB)
    nbins : int
           Number of histogram bins.
    clip_limit : float, optional (default is 0.01)
           Clipping limit where higher value increases contrast.

    Returns
    -------
    PIL.Image.Image
         image with contrast enhanced by adaptive equalization.
    """

    def __call__(self, img, nbins, clip_limit):
        adaptive_equ = F.adaptive_equalization(img, nbins, clip_limit)
        return adaptive_equ

    def __repr__(self):
        return self.__class__.__name__ + "()"


# ------- LocalEqualization input must be 2D (grayscale)


class LocalEqualization(object):
    """Filter gray image using local equalization.

    Local equalization method uses local histograms based on a disk structuring element.

    Parameters
    ---------
    img: PIL.Image.Image
        Input image. Notice that it must be 2D
    disk_size: int, optional (default is 50)
        Radius of the disk structuring element used for the local histograms

    Returns
    -------
    PIL.Image.Image
        2D image with contrast enhanced using local equalization.
    """

    def __call__(self, img, disk_size):
        local_equ = F.local_equalization(img, disk_size)
        return local_equ

    def __repr__(self):
        return self.__class__.__name__ + "()"


class KmeansSegmentation(object):
    """Segment an RGB image with K-means segmentation

    By using K-means segmentation (color/space proximity) each segment is
    colored based on the average color for that segment.

    Parameters
    ---------
    img : PIL.Image.Image
        Input image
    compactness : int, optional (default is 10)
        Color proximity versus space proximity factor.
    n_segments : int, optional (default is 800)
        The number of segments.

    Returns
    -------
    PIL.Image.Image
        Image where each segment has been colored based on the average
        color for that segment.
    """

    def __call__(self, img, compactness, n_segment):
        kmeans_segmentation = F.kmeans_segmentation(img, compactness, n_segment)
        return kmeans_segmentation

    def __repr__(self):
        return self.__class__.__name__ + "()"


class RagThreshold(object):
    """Combine similar K-means segmented regions based on threshold value.

    Segment an image with K-means, build region adjacency graph based on
    the segments, combine similar regions based on threshold value,
    and then output these resulting region segments.

    Parameters
    ----------
    img : PIL.Image.Image
        Input image
    compactness : int, optional (default is 10)
        Color proximity versus space proximity factor.
    n_segments :  int, optional (default is 800)
        The number of segments.
    threshold : int, optional (default is 9)
        Threshold value for combining regions.

    Returns
    -------
    PIL.Image.Image
        Each segment has been colored based on the average
        color for that segment (and similar segments have been combined).
    """

    def __call__(self, img, compactness, n_segments, threshold):
        return F.rag_threshold(img, compactness, n_segments, threshold)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class HysteresisThreshold(object):
    """Apply two-level (hysteresis) threshold to an image.

    Parameters
    ----------
    img : PIL.Image.Image
        Input image
    low : int, optional (default is 50)c
        low threshold
    high : int, optional (default is 100)
        high threshold

    Returns
    -------
    PIL.Image.Image
        Boolean mask where True represents pixel above
        the hysteresis threshold
    """

    def __call__(self, img, low: int = 50, high: int = 100):
        return F.hysteresis_threshold(img, low, high)

    def __repr__(self):
        return self.__class__.__name__ + "()"


# ----------- Branching functions (grayscale/invert input)-------------------

# invert --> grayscale ..> hysteresis
class HysteresisThresholdMask(object):
    """Mask an image using hysteresis threshold

    Compute the Hysteresis threshold on the complement of a greyscale image,
    and return boolean mask based on pixels above this threshold.

    Parameters
    ----------
    img : PIL.Image.Image
        Input image.
    low : int, optional (default is 50)
        low threshold
    high : int, optional (default is 100)
         high threshold

    Returns
    -------
    np.ndarray
     Boolean NumPy array where True represents a pixel above Otsu threshold.
    """

    def __call__(self, img, low, high):
        hysteresis_threshold_mask = F.hysteresis_threshold_mask(img, low, high)
        return hysteresis_threshold_mask

    def __repr__(self):
        return self.__class__.__name__ + "()"


class OtsuThreshold(object):
    """Mask image based on pixel above Otsu threshold.

    Compute Otsu threshold on image as a NumPy array and return boolean mask
    based on pixels above this threshold.

    Note that Otsu threshold is expected to work correctly only for grayscale images

    Parameters
    ----------
    img : PIL.Image.Image
        Input image.

    Returns
    -------
    np.ndarray
        Boolean NumPy array where True represents a pixel above Otsu threshold.
    """

    def __call__(self, img):
        return F.otsu_threshold(img)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class LocalOtsuThreshold(object):
    """Mask image based on local Otsu threshold.

    Compute local Otsu threshold for each pixel and return boolean mask
    based on pixels being less than the local Otsu threshold.

    Note that the input image must be 2D.

    Parameters
    ----------
    img: PIL.Image.Image
        Input 2-dimensional image
    disk_size :int, optional (default is 3)
        Radius of the disk structuring element used to compute
        the Otsu threshold for each pixel.

    Returns
    -------
    np.ndarray
        NumPy boolean array representing the mask based on local Otsu threshold
    """

    def __call__(self, img, disk_size):
        return F.local_otsu_threshold(img, disk_size)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class FilterEntropy(object):
    """Filter image based on entropy (complexity).

    The area of the image included in the local neighborhood is defined by a square
    neighborhoodxneighborhood

    Note that input must be 2D.

    Parameters:
    ----------
    img : PIL.Image.Image
        input 2-dimensional image
    neighborhood : int, optional (default is 9)
        Neighborhood size (defines height and width of 2D array of 1's).
    threshold : int, optional (default is 9)
        Threshold value.

    Returns
    -------
    np.ndarray
        NumPy boolean array where True represent a measure of complexity.
    """

    def __call__(self, img, neighborhood, threshold):
        return F.filter_entropy(img, neighborhood, threshold)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class CannyEdges(object):
    """Filter image based on Canny edge algorithm.

    Note that input image must be 2D

    Parameters
    ----------
    img : PIL.Image.Image
        Input 2-dimensional image
    sigma : float, optional (default is 1.0)
        Width (std dev) of Gaussian.
    low_threshold : float, optional (default is 0.0)
        Low hysteresis threshold value.
    high_threshold : float, optional (default is 25.0)
        High hysteresis threshold value.

    Returns
    -------
    np.ndarray
        Boolean NumPy array representing Canny edge map.
    """

    def __call__(self, img, sigma, low_threshold, high_threshold):
        return F.canny_edges(img, sigma, low_threshold, high_threshold)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class Grays(object):
    """Filter out gray pixels in RGB image.

    Grey pixels are those pixels where the red, green, and blue channel values
    are similar, i.e. under a specified tolerance.

    Parameters
    ----------
    img : PIL.Image.Image
        Input image
    tolerance : int, optional (default is 15)
        if difference between values is below this threshold,
        values are considered similar and thus filtered out

    Returns
    -------
    PIL.Image.Image
        Mask image where the grays values are masked out"""

    def __call__(self, img, tolerance):
        return F.grays(img, tolerance)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class GreenChannelFilter(object):
    """Mask pixels in an RGB image with G-channel greater than a specified threshold.

    Create a mask to filter out pixels with a green channel value greater than
    a particular threshold, since hematoxylin and eosin are purplish and pinkish,
    which do not have much green to them.

    Parameters
    ----------
    img : PIL.Image.Image
        Input RGB image
    green_thresh : float, optional (default is 200.0)
        Green channel threshold value (0 to 255).
        If value is greater than green_thresh, mask out pixel.
    avoid_overmask : bool, optional (default is True)
        If True, avoid masking above the overmask_thresh percentage.
    overmask_thresh : float, optional (default is 90.0)
        If avoid_overmask is True, avoid masking above this percentage value.

    Returns
    -------
    np.ndarray
        Boolean mask where pixels above a particular green channel
        threshold have been masked out.
    """

    def __call__(self, img, green_thresh, avoid_overmask, overmask_thresh):
        return F.green_channel_filter(
            img, green_thresh, avoid_overmask, overmask_thresh
        )

    def __repr__(self):
        return self.__class__.__name__ + "()"


class RedFilter(object):
    """Mask reddish colors in an RGB image.

    Create a mask to filter out reddish colors, where the mask is based on a pixel
    being above a red channel threshold value, below a green channel threshold value,
    and below a blue channel threshold value.

    Parameters
    ----------
    img : PIl.Image.Image
        Input RGB image
    red_lower_thresh : float
        Red channel lower threshold value.
    green_upper_thresh : float
        Green channel upper threshold value.
    blue_upper_thresh : float
        Blue channel upper threshold value.

    Returns
    -------
    np.ndarray
        Boolean NumPy array representing the mask.
    """

    def __call__(self, img, red_thresh, green_thresh, blue_thresh):
        return F.red_filter(img, red_thresh, green_thresh, blue_thresh)


class RedPenFilter(object):
    """Filter out red pen marks on diagnostic slides.

    The resulting mask is a composition of red filters with different thresholds
    for the RGB channels.

    Parameters
    ----------
    img : PIL.Image.Image
        Input RGB image.

    Returns
    -------
        Boolean NumPy array representing the mask with the pen marks filtered out.
    """

    def __call__(self, img):
        return F.red_pen_filter(img)


class GreenFilter(object):
    """Filter out greenish colors in an RGB image.
    The mask is based on a pixel being above a red channel threshold value, below a
    green channel threshold value, and below a blue channel threshold value.

    Note that for the green ink, the green and blue channels tend to track together, so
    for blue channel we use a lower threshold rather than an upper threshold value.

    Parameters
    ----------
    img : PIL.image.Image
        RGB input image.
    red_thresh : int
        Red channel upper threshold value.
    green_thresh : int
        Green channel lower threshold value.
    blue_thresh : int
        Blue channel lower threshold value.

    Returns
    -------
    np.ndarray
        Boolean  NumPy array representing the mask.
    """

    def __call__(self, img, red_thresh, green_thresh, blue_thresh):
        return F.green_filter(img, red_thresh, green_thresh, blue_thresh)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class GreenPenFilter(object):
    """Filter out green pen marks from a diagnostic slide.

    The resulting mask is a composition of green filters with different thresholds
    for the RGB channels.

    Parameters
    ---------
    img : PIL.Image.Image
        Input RGB image

    Returns
    -------
    np.ndarray
        NumPy array representing the mask with the green pen marks filtered out.
    """

    def __call__(self, img):
        return F.green_pen_filter(img)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class BlueFilter(object):
    """Filter out blueish colors in an RGB image.

    Create a mask to filter out blueish colors, where the mask is based on a pixel
    being above a red channel threshold value, above a green channel threshold value,
    and below a blue channel threshold value.

    Parameters
    ----------
    img : PIl.Image.Image
        Input RGB image
    red_thresh : int
        Red channel lower threshold value.
    green_thresh : int
        Green channel lower threshold value.
    blue_thresh : int
        Blue channel upper threshold value.

    Returns
    -------
    np.ndarray
        Boolean NumPy array representing the mask.
    """

    def __call__(self, img, red_thresh, green_thresh, blue_thresh):
        return F.blue_filter(img, red_thresh, green_thresh, blue_thresh)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class BluePenFilter(object):
    """Filter out blue pen marks from a diagnostic slide.

    The resulting mask is a composition of green filters with different thresholds
    for the RGB channels.

    Parameters
    ---------
    img : PIL.Image.Image
        Input RGB image

    Returns
    -------
    np.ndarray
        NumPy array representing the mask with the blue pen marks filtered out.
    """

    def __call__(self, img):
        return F.blue_pen_filter(img)

    def __repr__(self):
        return self.__class__.__name__ + "()"


class PenMarks(object):
    """Filter out pen marks from a diagnostic slide.

    Pen amrks are removed by applying Otsu threshold on the H channel of the image
    converted to the HSV space.

    Parameters
    ---------
    img : PIL.Image.Image
        Input RGB image

    Returns
    -------
    np.ndarray
        Boolean NumPy array representing the mask with the pen marks filtered out.
    """

    def __call__(self, img):
        return F.pen_marks(img)

    def __repr__(self):
        return self.__class__.__name__ + "()"