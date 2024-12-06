import pytest
import responses
import requests
from dotenv import load_dotenv
from olympiabhub import OlympiaAPI


@pytest.fixture
def api():
    load_dotenv()
    model_name = "test_model"
    return OlympiaAPI(model=model_name)


@responses.activate
def test_chat_nubonyxia(api):
    prompt = "test_prompt"
    expected_response = {"response": "test_response"}

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/generate",
        json=expected_response,
        status=200,
    )

    result = api.ChatNubonyxia(prompt)
    assert result == expected_response
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.olympia.bhub.cloud/generate"
    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_chat(api):
    prompt = "test_prompt"
    expected_response = {"response": "test_response"}

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/generate",
        json=expected_response,
        status=200,
    )

    result = api.Chat(prompt)
    assert result == expected_response
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.olympia.bhub.cloud/generate"
    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_chat_nubonyxia_request_failure(api):
    prompt = "test_prompt"

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/generate",
        json={"error": "test_error"},
        status=400,
    )

    with pytest.raises(requests.exceptions.RequestException):
        api.ChatNubonyxia(prompt)


@responses.activate
def test_chat_request_failure(api):
    prompt = "test_prompt"

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/generate",
        json={"error": "test_error"},
        status=400,
    )

    with pytest.raises(requests.exceptions.RequestException):
        api.Chat(prompt)


@responses.activate
def test_create_embedding(api):
    texts = ["test_text1", "test_text2"]
    expected_response = {"embeddings": [[0.1, 0.2], [0.3, 0.4]]}

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/embedding",
        json=expected_response,
        status=200,
    )

    result = api.create_embedding(texts)
    assert result == expected_response
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.olympia.bhub.cloud/embedding"
    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_create_embedding_request_failure(api):
    texts = ["test_text1", "test_text2"]

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/embedding",
        json={"error": "test_error"},
        status=400,
    )

    with pytest.raises(requests.exceptions.RequestException):
        api.create_embedding(texts)


@responses.activate
def test_get_llm_models(api):
    expected_response = {"modèles": ["model1", "model2"]}

    responses.add(
        responses.GET,
        "https://api.olympia.bhub.cloud/modeles",
        json=expected_response,
        status=200,
    )

    result = api.get_llm_models()
    assert result == expected_response["modèles"]
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.olympia.bhub.cloud/modeles"
    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_get_llm_models_request_failure(api):
    responses.add(
        responses.GET,
        "https://api.olympia.bhub.cloud/modeles",
        json={"error": "test_error"},
        status=400,
    )

    with pytest.raises(requests.exceptions.RequestException):
        api.get_llm_models()


@responses.activate
def test_get_embedding_models(api):
    expected_response = {"modèles": ["embedding1", "embedding2"]}

    responses.add(
        responses.GET,
        "https://api.olympia.bhub.cloud/embedding/models",
        json=expected_response,
        status=200,
    )

    result = api.get_embedding_models()
    assert result == expected_response["modèles"]
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.olympia.bhub.cloud/embedding/models"
    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_get_embedding_models_request_failure(api):
    responses.add(
        responses.GET,
        "https://api.olympia.bhub.cloud/embedding/models",
        json={"error": "test_error"},
        status=400,
    )

    with pytest.raises(requests.exceptions.RequestException):
        api.get_embedding_models()


@responses.activate
def test_create_embedding_nubonyxia(api):
    texts = ["test_text1", "test_text2"]
    expected_response = {"embeddings": [[0.1, 0.2], [0.3, 0.4]]}

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/embedding",
        json=expected_response,
        status=200,
    )

    result = api.create_embedding_nubonyxia(texts)
    assert result == expected_response
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.olympia.bhub.cloud/embedding"
    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_create_embedding_nubonyxia_request_failure(api):
    texts = ["test_text1", "test_text2"]

    responses.add(
        responses.POST,
        "https://api.olympia.bhub.cloud/embedding",
        json={"error": "test_error"},
        status=400,
    )

    with pytest.raises(requests.exceptions.RequestException):
        api.create_embedding_nubonyxia(texts)
