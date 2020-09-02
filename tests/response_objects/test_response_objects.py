import pytest

from rentomatic.domain.request_objects import room_list_request_object as req
from rentomatic.domain.response_objects import response_objects as res

# The first part contains just the imports and some pytest fixtures to make it easier to write the tests


@pytest.fixture
def response_value():
    return {"key": ["value1", "value2"]}


@pytest.fixture
def response_type():
    return "ResponseError"


@pytest.fixture
def response_message():
    return "This is a response error"


# The first two tests check that ResponseSuccess can be used as a boolean (this test was already present),
# that it provides a type, and that it can store a value.


def test_response_success_is_true(response_value):
    assert bool(res.ResponseSuccess(response_value)) is True


def test_response_success_has_type_and_value(response_value):
    response = res.ResponseSuccess(response_value)

    assert response.type == res.ResponseSuccess.SUCCESS
    assert response.value == response_value


# The remaining tests are all about ResponseFailure.

# A test to check that it behaves like a boolean


def test_response_failure_is_false(response_type, response_message):
    assert bool(res.ResponseFailure(response_type, response_message)) is False


# A second test to verify the class exposes a value attribute that contains both the type and the message.


def test_response_failure_has_type_and_message(response_type, response_message):
    response = res.ResponseFailure(response_type, response_message)

    assert response.type == response_type
    assert response.message == response_message


def test_response_failure_contains_value(response_type, response_message):
    response = res.ResponseFailure(response_type, response_message)

    assert response.value == {"type": response_type, "message": response_message}


# We sometimes want to create responses from Python exceptions that can happen in a use case,
# so we test that ResponseFailure objects can be initialised with a generic exception.
# We also check that the message is formatted properly


def test_response_failure_initialisation_with_exception(response_type):
    response = res.ResponseFailure(response_type, Exception("Just an error message"))

    assert bool(response) is False
    assert response.type == response_type
    assert response.message == "Exception: Just an error message"


# We want to be able to build a response directly from an invalid request,
# getting all the errors contained in the latter.


def test_response_failure_from_empty_invalid_request_object():
    response = res.ResponseFailure.build_from_invalid_request_object(req.InvalidRequestObject())

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR


def test_response_failure_from_invalid_request_object_with_errors():
    request_object = req.InvalidRequestObject()
    request_object.add_error("path", "Is mandatory")
    request_object.add_error("path", "can't be blank")
    response = res.ResponseFailure.build_from_invalid_request_object(request_object)

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.message == "path: Is mandatory\npath: can't be blank"


# The last three tests check that the ResponseFailure can create three specific errors,
# represented by the RESOURCE_ERROR, PARAMETERS_ERROR, and SYSTEM_ERROR class attributes.
# This categorization is an attempt to capture the different types of issues that can happen
# when dealing with an external system through an API.

# RESOURCE_ERROR contains all those errors that are related to the resources contained in the repository,
# for instance when you cannot find an entry given its unique ID.

# PARAMETERS_ERROR describes all those errors that occur when the request parameters are wrong or missing.

# SYSTEM_ERROR encompass the errors that happen in the underlying system at an operating system level,
# such as a failure in a filesystem operation, or a network connection error while fetching data from the database.


def test_response_failure_build_resource_error():
    response = res.ResponseFailure.build_resource_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.RESOURCE_ERROR
    assert response.message == "test message"


def test_response_failure_build_parameters_error():
    response = res.ResponseFailure.build_parameters_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.PARAMETERS_ERROR
    assert response.message == "test message"


def test_response_failure_build_system_error():
    response = res.ResponseFailure.build_system_error("test message")

    assert bool(response) is False
    assert response.type == res.ResponseFailure.SYSTEM_ERROR
    assert response.message == "test message"
