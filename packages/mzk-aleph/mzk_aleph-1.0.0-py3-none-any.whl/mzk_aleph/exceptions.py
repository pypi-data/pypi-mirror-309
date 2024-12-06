class MultipleRecordsFoundError(Exception):
    def __init__(self):
        super().__init__(
            message="Multiple records found when only one was expected.",
        )
