from typing import Dict
from robotlibcore import keyword
from RobotframeworkYetAnotherOcrLibrary.exception.ocr_error import OcrError
from RobotframeworkYetAnotherOcrLibrary.model.object_detection import ObjectDetection
from RobotframeworkYetAnotherOcrLibrary.opencv.algorithm import Algorithm
from RobotframeworkYetAnotherOcrLibrary.opencv.template_matching import TemplateMatching


class DetectionKeywords:
    """
    Robotframework interface for detection keywords.
    """

    def __init__(self):
        self._template_matching = TemplateMatching()

    @keyword
    def find_object(self, image_path: str, search_image: str, params: Dict) -> ObjectDetection:
        """
        Try to find an object from an image.

        :param image_path: (string) Filepath to image to search
        :param search_image: (string) Path from search object to find in image
        :param params: (Dict) Custom dictionary configuration parameters
        :return: Best object detection which contains the threshold and position

        :raise OcrError: MissingParams - If any kind of parameter is not set
        :raise OcrError: ImageNotFound - If image could not be load
        :raise OcrError: ObjectNotFound - If searched image could not be found from image

        Additional Parameters:
        | Name       | Default | Description                                |
        | algorithm  | 0       | Algorithm usage from supported Algorithms  |
        | threshold  | 90 %    | Threshold as number between 0 and 100 % for a similarity score.  |

        Template Matching params:
        | Name  | Default           | Description                     |
        | sizes | [(width, height)] | Array of size tuples to check.  |

        Examples:
        | Find Image On Screen  ../img/taskbar.jpg  ../img/jetbrains.jpg  ${TEMPLATE_MATCHING_TEST_PARAMS} |

        For an easier handling a variables.py will be recommended. Example variables.py:
        | TEMPLATE_MATCHING_TEST_PARAMS = {"threshold": 85, "sizes": [(16, 16), (32, 32), (64, 64), (256, 256)]} |
        """

        if params is None:
            params = {
                "algorithm": Algorithm.TemplateMatching,
                "threshold": 90
            }

        if "algorithm" not in params:
            params["algorithm"] = Algorithm.TemplateMatching

        if "threshold" not in params:
            params["threshold"] = 90

        if params["algorithm"] == Algorithm.TemplateMatching:
            object_position = self._template_matching.match(image_path, search_image, params)
            return object_position

        OcrError.raise_error(OcrError.NotSupportedOperation)
