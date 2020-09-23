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
from __future__ import annotations

from typing import Optional, Mapping, Any

class SearchResult:
	"""
	Small object that represents a search result.

	Attributes
	----------
	title : :class:`str`
		The title of the returned result.
	snippet : Optional[:class:`str`]
		A short description of the following website, if applicable.
	link : :class:`str`
		The target link.
	image : :class:`str`
		A preview image of the website, if applicable.
	"""

	__slots__ = ("title", "snippet", "link", "image")

	def __init__(self, data: Mapping[str, Any]):
		self.title: str = data['title']
		snip = data.get("snippet")
		self.snippet: Optional[str] = snip and ''.join(snip.split('\n'))
		self.link: str = data['link']
		image = data['pagemap'].get('cse_image')
		self.image: Optional[str] = image and image[0]['src']

	def __repr__(self) -> str:
		return "<SearchResult title={0.title!r} snippet={0.snippet!r} link={0.link!r} image={0.image!r}>".format(self)

	def __eq__(self, other: object) -> bool:
		return isinstance(other, SearchResult) and self.title == other.title
