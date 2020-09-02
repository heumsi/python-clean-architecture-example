from rentomatic.domain.request_objects import room_list_request_object as req


class ResponseFailure:
    RESOURCE_ERROR = "ResourceError"
    PARAMETERS_ERROR = "ParametersError"
    SYSTEM_ERROR = "SystemError"

    def __init__(self, type_: str, message: str) -> None:
        self.type = type_  # type 이 예약어라 끝에 _를 붙임
        self.message = self._format_message(message)

    def _format_message(self, msg: str) -> str:
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    @property
    def value(self) -> dict:
        return {"type": self.type, "message": self.message}

    def __bool__(self) -> bool:
        return False

    @classmethod
    def build_from_invalid_request_object(cls, invalid_request_object: req.InvalidRequestObject):
        message = "\n".join(
            ["{}: {}".format(err["parameter"], err["message"]) for err in invalid_request_object.errors]
        )

        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_resource_error(cls, message: str = None):
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message: str = None):
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message: str = None):
        return cls(cls.PARAMETERS_ERROR, message)


class ResponseSuccess:
    SUCCESS = "Success"

    def __init__(self, value=None) -> None:
        self.type = self.SUCCESS
        self.value = value

    def __bool__(self) -> bool:
        return True
