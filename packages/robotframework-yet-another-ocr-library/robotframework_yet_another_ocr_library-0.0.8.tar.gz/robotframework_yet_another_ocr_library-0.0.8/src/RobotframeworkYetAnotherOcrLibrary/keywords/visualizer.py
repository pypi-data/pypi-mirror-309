import base64
import cv2
from typing import Dict
from robotlibcore import keyword
from RobotframeworkYetAnotherOcrLibrary.exception.ocr_error import OcrError
from RobotframeworkYetAnotherOcrLibrary.model.object_detection import ObjectDetection
from RobotframeworkYetAnotherOcrLibrary.robotframework.robotlog import RobotLogger


class VisualizerKeywords:
    """
    Robotframework interface for visualizer keywords.
    """

    @keyword
    def visualize_object(self, image_path: str, object_detection: ObjectDetection, params: Dict = None) -> None:
        """
        Display object detection results in a window. Should be used for debugging purpose. For automation usage keyword
        Snapshot Object should be used to verify results in reports.

        :param image_path: (string) Filepath to image to use for a snapshot.
        :param object_detection: (ObjectDetection) Object detection to locate and include in a snapshot.
        :param params: (Dict) Dictionary of additional visualization parameters.

        Additional Parameters:
        | Name  | Default | Description                                |
        | size  | None    | Size from image which should be used to visualize as tuple for example (1024, 768)  |
        """
        image = cv2.imread(image_path)

        if image is None:
            OcrError.raise_error(OcrError.ImageNotFound.format(image_path))

        if object_detection:
            x = object_detection.x
            y = object_detection.y
            height = object_detection.height
            width = object_detection.width
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        if "size" in params:
            image = cv2.resize(image, params['size'], interpolation=cv2.INTER_LINEAR)

        cv2.imshow('Detected Positions', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @keyword
    def snapshot_object(self, image_path: str, object_detection: ObjectDetection) -> None:
        """
        Create a snapshot and include image into reporting log from robot.

        :param image_path: (string) Filepath to image to use for a snapshot.
        :param object_detection: (ObjectDetection) Object detection to locate and include in a snapshot.
        """
        image = cv2.imread(image_path)

        if image is None:
            OcrError.raise_error(OcrError.ImageNotFound.format(image_path))

        if object_detection:
            x = object_detection.x
            y = object_detection.y
            height = object_detection.height
            width = object_detection.width
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        success, encoded_image = cv2.imencode('.jpg', image)

        if success:
            base64_image = base64.b64encode(encoded_image).decode('utf-8')
            RobotLogger.log_screenshot_base64(base64_image)
            return

        OcrError.raise_error(OcrError.SnapshotNotCreated)
