import os
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from robot.api import logger


class RobotLogger:

    @staticmethod
    def get_log_directory():
        """
        Get output directory from robot framework built in variables if not exists fallback to os path execution
        """
        try:
            return BuiltIn().get_variable_value("${OUTPUT DIR}")
        except RobotNotRunningError:
            return os.getcwd()

    @staticmethod
    def log_screenshot_base64(image: str):
        """
        Append testing log by a screenshot in base64 format.

        ``image`` Image as string in base64 encoding.
        """
        logger.info(
            '</td></tr><tr><td colspan="3">' +
            f'<img src="data:image/png;base64,{image}" width="800px"/>',
            html=True
        )
