import cv2
from typing import Dict, Sequence
from YetAnotherOcrLibrary.exception.ocr_error import OcrError
from YetAnotherOcrLibrary.model.object_detection import ObjectDetection
from YetAnotherOcrLibrary.util.data_type import DataType


class TemplateMatching:
    """
    Template matching algorithm to find all similar images
    """

    def match(self, image_path: str, search_image_path: str, detection_params: Dict) -> None | ObjectDetection:
        """
        Template matching algorithm to find all similar images from a search image path.

        Following detection params are supported

        detection_params["threshold"] : number : Number between 0 and 100 to indicate a matching threshold
        detection_params["sizes] : list<[number, number]> : optional list of size (width, height)

        :param image_path: Image path to search objects
        :param search_image_path: Search image path to find object in image
        :param detection_params: Additional parameters to configure additional detection params.
        :return: None if object could not be found otherwise a detected object with position.
        """
        if "threshold" not in detection_params:
            OcrError.raise_error(OcrError.MissingParams.format("threshold"))

        sizes = None
        if "sizes" in detection_params:
            sizes = detection_params["sizes"]
            if not DataType.is_list_of_tuples(sizes):
                OcrError.raise_error("Sizes has to be a list of tuples which contains (width, height)")

        image = cv2.imread(image_path)

        if image is None:
            OcrError.raise_error(OcrError.ImageNotFound.format(image_path))

        threshold = detection_params["threshold"]
        tm_threshold = round(((threshold / 100) - 1) * -1, 2)

        search_image = cv2.imread(search_image_path)
        results = []

        if search_image is None:
            OcrError.raise_error(OcrError.ImageNotFound.format(search_image_path))

        if sizes:
            for size in sizes:
                search_image = cv2.resize(search_image, (size[0], size[1]), interpolation=cv2.INTER_CUBIC)
                min_val, max_val, min_loc, max_loc = self._match(image, search_image)
                results.append([min_val, max_val, min_loc, max_loc, (size[0], size[1])])
        else:
            height, width, channels = search_image.shape
            min_val, max_val, min_loc, max_loc = self._match(image, search_image)
            results.append([min_val, max_val, min_loc, max_loc, (height, width)])

        min_val, max_val, min_loc, max_loc, size = min(results, key=lambda x: x[0])

        if min_val < tm_threshold:
            return ObjectDetection(min_loc[0], min_loc[1], size[0], size[1], round((min_val - 1) * -1 * 100, 0))

        return None

    @staticmethod
    def _match(image: cv2, search_image: cv2) -> tuple[float, float, Sequence[int], Sequence[int]]:
        """
        Template matching algorithm to find all similar images from a search image path.

        :param image: Loaded cv2 image to search objects
        :param search_image: Loaded cv2 image to search object in image
        :return: Result as tuple which contains a minVal, maxVal, minLoc, maxLoc
        """
        result = cv2.matchTemplate(image, search_image, cv2.TM_SQDIFF_NORMED)
        return cv2.minMaxLoc(result)
