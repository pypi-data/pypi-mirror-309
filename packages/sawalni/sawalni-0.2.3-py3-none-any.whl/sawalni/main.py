from typing import List, Union, Dict, Any, Optional
import requests
import os
import openai

SAWALNI_API_KEY = os.getenv("SAWALNI_API_KEY")


class Sawalni:
    """Client for the Sawalni API with support for batched operations and retries."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.sawalni.com",
        max_retries: int = 3,
        show_progress: bool = True,
    ):
        """Initialize the Sawalni client.

        Args:
            api_key: API key for authentication. If not provided, reads from SAWALNI_API_KEY env var
            base_url: Base URL for the API. Defaults to https://api.sawalni.com
            max_retries: Maximum number of retries for failed requests. Defaults to 3
            show_progress: Whether to show progress bars for batch operations. Defaults to True
        """
        self.api_key = api_key or SAWALNI_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key must be provided either through the constructor or SAWALNI_API_KEY environment variable."
            )
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        self.max_retries = max_retries
        self.show_progress = show_progress

    def _request_with_retry(
        self, method: str, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make an API request with automatic retries on failure.

        Uses exponential backoff between retries, with a minimum wait of 4 seconds
        and maximum of 10 seconds between attempts.
        """
        from tenacity import retry, stop_after_attempt, wait_exponential

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=10),
        )
        def _make_request():
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()["data"]

        return _make_request()

    def _batch_process(
        self,
        items: List[Any],
        batch_size: int,
        process_fn: callable,
        desc: str = "Processing",
    ) -> List[Any]:
        """Process a list of items in batches with progress tracking.

        Args:
            items: List of items to process
            batch_size: Number of items to process in each batch
            process_fn: Function to process each batch
            desc: Description for the progress bar

        Returns:
            List of processed results
        """
        from tqdm import tqdm

        results = []

        iterator = (
            tqdm(range(0, len(items), batch_size), desc=desc)
            if self.show_progress
            else range(0, len(items), batch_size)
        )
        for i in iterator:
            batch = items[i : i + batch_size]
            try:
                result = process_fn(batch)
                results.extend(result if isinstance(result, list) else [result])
            except Exception as e:
                print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
                raise

        return results

    def answer(
        self,
        query: Union[str, List[str]],
        model: str = "sawalni-mini",
        temperature: float = 0.7,
    ) -> Union[str, List[str]]:
        """Generate replies to queries. Processes one query at a time."""
        if isinstance(query, str):
            data = {
                "messages": [{"role": "user", "content": query}],
                "model": model,
                "temperature": temperature,
            }
            response = self.chat.completions.create(**data)
            return response.choices[0].message.content

        return self._batch_process(
            query,
            batch_size=1,
            process_fn=lambda q: self.answer(q[0], model, temperature),
            desc="Generating answers",
        )

    def embed(
        self, input: Union[str, List[str]], model: str = "madmon-mini"
    ) -> Dict[str, Any]:
        """Generate multilingual embeddings for text. Processes in batches of 32."""
        if isinstance(input, str):
            return self._request_with_retry(
                "POST", "/v1/embeddings", {"input": input, "model": model}
            )

        return self._batch_process(
            input,
            batch_size=32,
            process_fn=lambda batch: self._request_with_retry(
                "POST", "/v1/embeddings", {"input": batch, "model": model}
            ),
            desc="Generating embeddings",
        )

    def search(
        self,
        query: Union[str, List[str]],
        model: str = "sawalni-mini",
        rerank: bool = False,
        stream: bool = False,
        extra_languages: Optional[List[str]] = None,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Search for information. Processes one query at a time."""
        if isinstance(query, str):
            data = {
                "query": query,
                "model": model,
                "rerank": rerank,
                "stream": stream,
                "extra_languages": extra_languages,
            }
            return self._request_with_retry("POST", "/v1/search", data)

        return self._batch_process(
            query,
            batch_size=1,
            process_fn=lambda q: self.search(
                q[0], model, rerank, stream, extra_languages
            ),
            desc="Searching",
        )

    def identify(
        self, input: Union[str, List[str]], model: str = "gherbal-mini", top: int = 1
    ) -> Dict[str, Any]:
        """Identify language of text. Processes in batches of 32."""
        if isinstance(input, str):
            return self._request_with_retry(
                "POST",
                "/v1/language/identify",
                {"input": input, "model": model, "top": top},
            )

        return self._batch_process(
            input,
            batch_size=32,
            process_fn=lambda batch: self._request_with_retry(
                "POST",
                "/v1/language/identify",
                {"input": batch, "model": model, "top": top},
            ),
            desc="Identifying languages",
        )

    def translate(
        self,
        input: Union[str, List[str]],
        source: str,
        target: str,
        model: str = "tarjamli-medium",
    ) -> Dict[str, Any]:
        """Translate text. Processes one text at a time."""
        if isinstance(input, str):
            return self._request_with_retry(
                "POST",
                "/v1/language/translate",
                {"text": input, "source": source, "target": target, "model": model},
            )

        return self._batch_process(
            input,
            batch_size=1,
            process_fn=lambda text: self.translate(text[0], source, target, model),
            desc="Translating",
        )

    def transliterate(
        self,
        input: Union[str, List[str]],
        model: str = "daktilo-mini",
        temperature: float = 0.1,
        to: str = "latn",
    ):
        """Transliterate text. Processes one text at a time."""
        if isinstance(input, str):
            data = {"text": input, "model": model, "to": to, "temperature": temperature}
            data = {k: v for k, v in data.items() if v is not None}
            return self._request_with_retry("POST", "/v1/language/transliterate", data)

        return self._batch_process(
            input,
            batch_size=1,
            process_fn=lambda text: self.transliterate(text[0], model, temperature, to),
            desc="Transliterating",
        )

    @property
    def chat(self) -> Any:
        """Get OpenAI client for chat completions."""
        client = openai.OpenAI(
            base_url="https://api.sawalni.com/v1", api_key=self.api_key
        )
        return client.chat

    @property
    def embeddings(self) -> Any:
        """Get OpenAI client for embeddings."""
        client = openai.OpenAI(
            base_url="https://api.sawalni.com/v1", api_key=self.api_key
        )
        return client.embeddings


class SawalniAsync:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.sawalni.com",
        max_retries: int = 3,
        show_progress: bool = True,
    ):
        self.api_key = api_key or SAWALNI_API_KEY
        if not self.api_key:
            raise ValueError(
                "API key must be provided either through the constructor or SAWALNI_API_KEY environment variable."
            )
        self.base_url = base_url
        self.max_retries = max_retries
        self.show_progress = show_progress

    async def _request_with_retry(
        self, method: str, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make an API request with automatic retries on failure."""
        from tenacity import retry, stop_after_attempt, wait_exponential
        import aiohttp

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=10),
        )
        async def _make_request():
            url = f"{self.base_url}{endpoint}"
            async with aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as session:
                async with session.request(method, url, json=data) as response:
                    response.raise_for_status()
                    return (await response.json())["data"]

        return await _make_request()

    async def _batch_process(
        self,
        items: List[Any],
        batch_size: int,
        process_fn: callable,
        desc: str = "Processing",
    ) -> List[Any]:
        """Process a list of items in batches with progress tracking."""
        from tqdm import tqdm

        results = []
        iterator = (
            tqdm(range(0, len(items), batch_size), desc=desc)
            if self.show_progress
            else range(0, len(items), batch_size)
        )
        for i in iterator:
            batch = items[i : i + batch_size]
            result = await process_fn(batch)
            results.append(result)
        return results

    async def answer(
        self, query: str, model: str = "sawalni-mini", temperature: float = 0.7
    ) -> Dict[str, Any]:
        data = {
            "messages": [{"role": "user", "content": query}],
            "model": model,
            "temperature": temperature,
        }
        response = await self._request_with_retry("POST", "/v1/chat/completions", data)
        return response["choices"][0]["message"]["content"]

    async def embed(
        self, input: Union[str, List[str]], model: str = "madmon-mini"
    ) -> Dict[str, Any]:
        if isinstance(input, str):
            data = {"input": input, "model": model}
            return await self._request_with_retry("POST", "/v1/embeddings", data)

        return await self._batch_process(
            input,
            batch_size=1,
            process_fn=lambda text: self.embed(text[0], model),
            desc="Embedding",
        )

    async def search(
        self,
        query: str,
        model: str = "sawalni-mini",
        rerank: bool = False,
        stream: bool = False,
        extra_languages: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        data = {
            "query": query,
            "model": model,
            "rerank": rerank,
            "stream": stream,
            "extra_languages": extra_languages,
        }
        return await self._request_with_retry("POST", "/v1/search", data)

    async def identify(
        self, input: Union[str, List[str]], model: str = "gherbal-mini", top: int = 1
    ) -> Dict[str, Any]:
        if isinstance(input, str):
            data = {"input": input, "model": model, "top": top}
            return await self._request_with_retry("POST", "/v1/language/identify", data)

        return await self._batch_process(
            input,
            batch_size=1,
            process_fn=lambda text: self.identify(text[0], model, top),
            desc="Identifying",
        )

    async def translate(
        self,
        input: Union[str, List[str]],
        source: str,
        target: str,
        model: str = "tarjamli-medium",
    ) -> Dict[str, Any]:
        if isinstance(input, str):
            return await self._request_with_retry(
                "POST",
                "/v1/language/translate",
                {"text": input, "source": source, "target": target, "model": model},
            )

        return await self._batch_process(
            input,
            batch_size=1,
            process_fn=lambda text: self.translate(text[0], source, target, model),
            desc="Translating",
        )

    async def transliterate(
        self,
        input: Union[str, List[str]],
        model: str = "daktilo-mini",
        temperature: float = 0.1,
        to: str = "latn",
    ):
        if isinstance(input, str):
            data = {"text": input, "model": model, "to": to, "temperature": temperature}
            data = {k: v for k, v in data.items() if v is not None}
            return await self._request_with_retry(
                "POST", "/v1/language/transliterate", data
            )

        return await self._batch_process(
            input,
            batch_size=1,
            process_fn=lambda text: self.transliterate(text[0], model, temperature, to),
            desc="Transliterating",
        )

    @property
    def chat(self) -> Any:
        client = openai.AsyncOpenAI(
            base_url="https://api.sawalni.com/v1", api_key=self.api_key
        )
        return client.chat

    @property
    def embeddings(self) -> Any:
        client = openai.AsyncOpenAI(
            base_url="https://api.sawalni.com/v1", api_key=self.api_key
        )
        return client.embeddings
