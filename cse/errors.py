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

from typing import Mapping

__all__ = ['SearchError', 'QuotaExceededError']

class SearchError(Exception):
	"""Raised when the API returns an error."""
	def __init__(self, data: Mapping[str, str]) -> None:
		super().__init__("[{code}: {status}] {message}".format(**data))

class QuotaExceededError(SearchError):
	"""Raised when the active API key has run out of uses."""
	def __init__(self) -> None:
		Exception.__init__(self, "100 queries/day quota has been exceeded for this API key")
