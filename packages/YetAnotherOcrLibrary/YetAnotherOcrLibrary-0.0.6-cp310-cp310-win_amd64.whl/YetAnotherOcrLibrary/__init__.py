from enum import Enum
from robotlibcore import DynamicCore
from robot.libraries.BuiltIn import BuiltIn
from YetAnotherOcrLibrary import version
from YetAnotherOcrLibrary.keywords.detection import DetectionKeywords
from YetAnotherOcrLibrary.keywords.visualizer import VisualizerKeywords


class YetAnotherOcrLibrary(DynamicCore):
    """
     YetAnotherOcrLibrary is a Robot Framework library for object recognition.

     == Library usage ==

     Library  YetAnotherOcrLibrary
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
            YetAnotherOcrLibrary.KeywordModules.Detection: DetectionKeywords(),
            YetAnotherOcrLibrary.KeywordModules.Visualizer: VisualizerKeywords(),
        }

        self.libraries = list(self.keyword_modules.values())
        DynamicCore.__init__(self, self.libraries)
