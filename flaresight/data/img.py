"""
Utilities for image processing.
"""
# standard library imports
import sys

# 3rd party imports
import numpy as np


class Rect:
    """
    A class for representing a rectangle.
    """

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> None:
        """
        Initialize the Rect class.

        Parameters
        ----------
        x: int
            The x-coordinate of the left side of the rectangle.
        y: int
            The y-coordinate of the top side of the rectangle.
        width: int
            The width of the rectangle.
        height: int
            The height of the rectangle.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self) -> str:
        """
        Return a string representation of the rectangle.

        Returns
        -------
        str
            String representation of the rectangle.
        """
        return "[x: {}, y: {}, width: {}, height: {}]".format(self.x, self.y, self.width, self.height)

    def __eq__(self, other) -> bool:
        """
        Check if two rectangles are equal.

        Parameters
        ----------
        other: Rect
            The other rectangle to compare to.

        Returns
        -------
        bool
            Whether the two rectangles are equal.
        """
        return (
            self.x == other.x
            and self.y == other.y
            and self.width == other.width
            and self.height == other.height
        )

    def set_from_yolo(self, yolo: list[float], img_width: int, img_height: int) -> None:
        """
        Convert a YOLO bounding box to a rectangle.

        Parameters
        ----------
        yolo: list
            The YOLO bounding box in the format [center_x, center_y, width, height].
        img_width: int
            The width of the image the bounding box is in.
        img_height: int
            The height of the image the bounding box is in.

        Returns
        -------
        None
        """
        center_x, center_y, width, height = yolo
        self.x = int((center_x - width / 2) * img_width)
        self.y = int((center_y - height / 2) * img_height)
        self.width = int(width * img_width)
        self.height = int(height * img_height)


class ROI:
    """
    A class for working with regions of interest.
    """

    def __init__(self, rect: Rect, label: str) -> None:
        """
        Initialize ROI.

        Parameters
        ----------
        rect: Rect
            The rectangle of the region of interest.
        label: str
            The label of the region of interest.

        Returns
        -------
        None
        """
        self._rect = rect
        self._label = label

    @property
    def box(self) -> Rect:
        """
        The rectangle of the region of interest.

        Parameters
        ----------
        None

        Returns
        -------
        Rect
            The rectangle of the region of interest.
        """
        return self._rect

    @property
    def label(self) -> str:
        """
        The label of the region of interest.

        Parameters
        ----------
        None

        Returns
        -------
        str
            The label of the region of interest.
        """
        return self._label

    def __str__(self) -> str:
        """
        Return a string representation of the region of interest.

        Returns
        -------
        str
            String representation of the region of interest.
        """
        return "{}: {}".format(self._label, self._rect)


class Image:
    """
    A class for working with images.
    """

    def __init__(self, image: np.ndarray, rois: list[ROI] = []) -> None:
        """
        Initialize Image.

        Parameters
        ----------
        image: np.ndarray
            The image to work with.

        Returns
        -------
        None
        """
        self._image = image
        self._rois = rois

    def get_ndarray(self) -> np.ndarray:
        """
        The image as a numpy array.

        Parameters
        ----------
        None

        Returns
        -------
        np.ndarray
            The image as a numpy array.
        """
        return self._image

    def set_ndarray(self, image: np.ndarray) -> None:
        """
        Set the image as a numpy array.

        Parameters
        ----------
        image: np.ndarray
            The image to set.

        Returns
        -------
        None
        """
        self._image = image

    @property
    def ndarray(self) -> np.ndarray:
        """
        The image as a numpy array.

        Parameters
        ----------
        None

        Returns
        -------
        np.ndarray
            The image as a numpy array.
        """
        return self._image

    @property
    def n_bytes(self) -> int:
        """
        Amount of memory used by the image in bytes.

        Parameters
        ----------
        None

        Returns
        -------
        int
            The number of bytes used by the image.
        """
        return sys.getsizeof(self._image)

    @property
    def width(self) -> int:
        """
        The width of the image.

        Parameters
        ----------
        None

        Returns
        -------
        int
            The width of the image.
        """
        return self._image.shape[1]

    @property
    def height(self) -> int:
        """
        The height of the image.

        Parameters
        ----------
        None

        Returns
        -------
        int
            The height of the image.
        """
        return self._image.shape[0]

    @property
    def depth(self) -> tuple:
        """
        The shape of the image.

        Parameters
        ----------
        None

        Returns
        -------
        tuple
            The shape of the image.
        """
        if self._image.ndim < 3:
            return 1
        else:
            return self._image.shape[2]

    def rgb_to_gray(self) -> np.ndarray:
        """
        Convert an RGB image to grayscale.

        Parameters
        ----------
        rgb_image: np.ndarray
            The RGB image to convert to grayscale.

        Returns
        -------
        np.ndarray
            The grayscale image.
        """
        rgb_to_gray = np.array([0.299, 0.587, 0.114])
        return (self._image @ rgb_to_gray).astype(np.uint8)

    def add_roi(self, roi: ROI) -> None:
        """
        Add a region of interest to the image.

        Parameters
        ----------
        roi: ROI
            The region of interest to add.

        Returns
        -------
        None
        """
        self._rois.append(roi)

    @property
    def rois(self) -> list[ROI]:
        """
        The regions of interest in the image.

        Parameters
        ----------
        None

        Returns
        -------
        list[ROI]
            The regions of interest in the image.
        """
        return self._rois
