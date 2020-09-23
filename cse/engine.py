"""
Copyright 2020 XuaTheGrate

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Any, List, Mapping, Optional
from urllib.parse import urlencode

import aiohttp

from .errors import *
from .flags import *
from .result import SearchResult

__all__ = ["Search"]

class Search:
	"""
	The search object used for interacting with the API.

	Attributes
	----------
	api_key : :class:`str`
		Your API key for interacting with the Google PSE API.
		You can obtain one via `this link <https://developers.google.com/custom-search/v1/overview>`_.
	session : Optional[:class:`ClientSession`]
		A client session to use. This is automatically closed with :meth:`Search.close`.
	engine_id : str
		The engine ID to use. Specifying a custom one is not required.
	"""
	__slots__ = ("session", "api_key", "engine_id")

	CSE_URL = "https://customsearch.googleapis.com/customsearch/v1?{}"

	def __init__(
			self,
			api_key: str, *,
			session: Optional[aiohttp.ClientSession] = None,
			engine_id: str = "0013301c62cb228c5"
		):
		self.session = session
		self.api_key = api_key
		self.engine_id = engine_id

	async def close(self) -> None:
		"""Closes the internal session."""
		if self.session is not None:
			await self.session.close()

	async def _search(self, params: str) -> Mapping[str, Any]:
		if self.session is None:
			self.session = aiohttp.ClientSession()
		async with self.session.get(self.CSE_URL.format(params)) as get:
			return await get.json()  # type: ignore

	async def search(
			self, 
			query: str, *,
			max_results: int = 10,
			start_index: int = 0,
			language: Optional[Language] = None,
			safe_search: bool = True
		) -> List[SearchResult]:
		"""Searches the API for your requested query.
		For image searching, use :meth:`cse.Search.image_search`.

		Parameters
		----------
		query : str
			The Google query to search for.
		max_results : int
			The maximum amount of results to return. Must be between 1 and 10.
		start_index : int
			The start index of results to return. Must be between 0 and 100.
			The default amount of results per-page is 10, so a start index of 11 would start the second page.
		language : Optional[:class:`cse.Language`]
			The language(s) to search for. Passing ``None`` is equivalent to English.
		safe_search : bool
			Whether to return NSFW results.

		Raises
		------
		:class:`ValueError`
			One or more arguments had an invalid value.
		:class:`cse.QuotaExceededError`
			The current API key has run out of requests.
		:class:`cse.SearchError`
			The API returned an error.

		Returns
		-------
		List[:class:`cse.SearchResult`]
			A list of all the search results. Can be empty.
		"""

		if 1 > max_results > 10:
			raise ValueError("\"max_results\" cannot be lower than 1 or higher than 10")

		if 0 > start_index > 100:
			raise ValueError("\"start_index\" cannot be less than 0 or higher than 100")

		params = {
			"q": query,
			"cx": self.engine_id,
			"key": self.api_key,
			"num": max_results,
			"start": start_index + 1,
			"safe": "active" if safe_search else "off"
		}

		if language is not None and language.to_google_flags() is not None:
			params['lr'] = language.to_google_flags()

		response = await self._search(urlencode(params))

		error = response.get("error")
		if error:
			if error.status == "RESOURCE_EXHAUSTED":
				raise QuotaExceededError()
			raise SearchError(response['error'])

		return [SearchResult(d) for d in response['items']]
