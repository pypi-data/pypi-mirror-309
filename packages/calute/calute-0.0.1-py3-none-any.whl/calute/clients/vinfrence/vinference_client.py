import urllib.parse
import json
from typing import Generator, Union, Optional
import requests
from calute.clients.vinfrence.types import (
	ChatCompletionRequest,
	ChatCompletionResponse,
	ChatCompletionStreamResponse,
)


class vInferenceAPIError(Exception):
	def __init__(
		self, status_code: int, message: str, response_content: Optional[str] = None
	):
		self.status_code = status_code
		self.message = message
		self.response_content = response_content
		super().__init__(f"vInference API Error ({status_code}): {message}")


class vInferenceChatCompletionClient:
	def __init__(
		self,
		base_url: str,
		max_retries: int = 5,
		timeout: float = 60.0,
		max_chunk_size: int = 4000,
	):
		url = urllib.parse.urlparse(base_url)
		self.base_url = f"{url.scheme}://{url.netloc}"
		self.max_retries = max_retries
		self.timeout = timeout
		self.max_chunk_size = max_chunk_size

		# Configure session with retries
		self.session = requests.Session()
		retry_strategy = requests.adapters.Retry(
			total=max_retries,
			backoff_factor=1,
			status_forcelist=[502, 503, 504],
			allowed_methods=["POST"],
		)
		adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
		self.session.mount("http://", adapter)
		self.session.mount("https://", adapter)

	def _parse_error_response(self, response: requests.Response) -> str:
		try:
			error_data = response.json()
			return error_data.get("error", {}).get("message", response.text)
		except (json.JSONDecodeError, AttributeError):
			return response.text

	def _chunk_messages(
		self, request: ChatCompletionRequest
	) -> list[ChatCompletionRequest]:
		"""Split request into smaller chunks if content length exceeds max_chunk_size."""
		total_length = sum(len(msg.content) for msg in request.messages)

		if total_length <= self.max_chunk_size:
			return [request]

		chunks = []
		current_messages = []
		current_length = 0

		for msg in request.messages:
			msg_length = len(msg.content)
			if current_length + msg_length > self.max_chunk_size and current_messages:
				new_request = request.model_copy(deep=True)
				new_request.messages = current_messages.copy()
				chunks.append(new_request)
				current_messages = []
				current_length = 0

			current_messages.append(msg)
			current_length += msg_length

		if current_messages:
			new_request = request.model_copy(deep=True)
			new_request.messages = current_messages
			chunks.append(new_request)

		return chunks

	def create_chat_completion(
		self,
		request: ChatCompletionRequest,
	) -> Generator[
		Union[ChatCompletionStreamResponse, ChatCompletionResponse],
		None,
		None,
	]:
		"""
		Create a chat completion with streaming response.

		Args:
		    request: ChatCompletionRequest object containing the request parameters

		Yields:
		    dict: Parsed response chunks from the API

		Raises:
		    vInferenceAPIError: If the API returns an error response
		    requests.RequestException: For network-related errors
		"""
		url = f"{self.base_url}/v1/chat/completions"

		headers = {
			"bypass-tunnel-reminder": "true",
			"Content-Type": "application/json",
			"Accept": "application/json",
		}

		out = ChatCompletionStreamResponse if request.stream else ChatCompletionResponse

		# Split request into chunks if necessary
		request_chunks = self._chunk_messages(request)

		for chunk in request_chunks:
			jsn_data = chunk.model_dump_json()

			try:
				with self.session.post(
					url,
					data=jsn_data,
					headers=headers,
					stream=True,
					timeout=self.timeout,
				) as response:
					if response.status_code != 200:
						error_message = self._parse_error_response(response)

						# Specific handling for common errors
						if response.status_code == 413:
							raise vInferenceAPIError(
								status_code=413,
								message="Payload too large. Try reducing message size or adjusting max_chunk_size.",
								response_content=response.text,
							)
						elif response.status_code == 500:
							raise vInferenceAPIError(
								status_code=500,
								message="Internal server error. The request may be too large or complex.",
								response_content=response.text,
							)
						else:
							raise vInferenceAPIError(
								status_code=response.status_code,
								message=error_message,
								response_content=response.text,
							)

					for line in response.iter_lines(decode_unicode=True):
						if line:
							if line.startswith("data: "):
								try:
									data = json.loads(line[6:])
									yield out(**data)
								except json.JSONDecodeError as e:
									raise vInferenceAPIError(
										status_code=response.status_code,
										message=f"Failed to parse response: {str(e)}",
										response_content=line,
									) from e
							else:
								try:
									data = json.loads(line)
									yield out(**data)
								except json.JSONDecodeError as e:
									raise vInferenceAPIError(
										status_code=response.status_code,
										message=f"Failed to parse response: {str(e)}",
										response_content=line,
									) from e

			except requests.RequestException as e:
				raise vInferenceAPIError(
					status_code=500, message=f"Network error occurred: {str(e)}"
				) from e

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.session.close()
