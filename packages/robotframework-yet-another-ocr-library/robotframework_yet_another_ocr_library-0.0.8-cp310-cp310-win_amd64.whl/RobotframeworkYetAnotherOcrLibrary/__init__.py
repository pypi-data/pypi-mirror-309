from enum import Enum
from robotlibcore import DynamicCore
from robot.libraries.BuiltIn import BuiltIn
from RobotframeworkYetAnotherOcrLibrary import version
from RobotframeworkYetAnotherOcrLibrary.keywords.detection import DetectionKeywords
from RobotframeworkYetAnotherOcrLibrary.keywords.visualizer import VisualizerKeywords


class RobotframeworkYetAnotherOcrLibrary(DynamicCore):
    """
     RobotframeworkYetAnotherOcrLibrary is a Robotframework library for object recognition.

     == Library usage ==

    Library  RobotframeworkYetAnotherOcrLibrary
    """

    ROBOT_LIBRARY_VERSION = version.VERSION
    ROBOT_LIBRARY_SCOPE = "Global"
    ROBOT_LISTENER_API_VERSION = 2

    class KeywordModules(Enum):
        """
        Enumeration from all supported keyword modules.
        """
        Detection = "Detection"
        Visualizer = "Visualizer"

    def __init__(self):
        self.builtin = BuiltIn()

        self.keyword_modules = {
            RobotframeworkYetAnotherOcrLibrary.KeywordModules.Detection: DetectionKeywords(),
            RobotframeworkYetAnotherOcrLibrary.KeywordModules.Visualizer: VisualizerKeywords(),
        }

        self.libraries = list(self.keyword_modules.values())
        DynamicCore.__init__(self, self.libraries)
