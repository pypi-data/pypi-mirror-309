class OcrError(Exception):
    """
    OcrError exception class which handles all object recognition errors.
    """
    MissingParams = "Missing parameter in usage '{}'"
    ImageNotFound = "Image '{}' could not be found"
    ObjectNotFound = "Could not find any object"
    NotSupportedOperation = "Not supported operation"
    SnapshotNotCreated = "Snapshot could not be created"

    @staticmethod
    def raise_error(message) -> None:
        """
        Static method usage to raise an OcrError error.

        :param message: (string) - Error message to raise.
        """
        raise OcrError(message) from None
