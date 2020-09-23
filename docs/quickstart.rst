.. currentmodule:: cse

Quickstart Guide
=================

This document will show you how to quickly set up the search engine.

Firstly, obtain an API key from `this link <https://developers.google.com/custom-search/v1/overview>`_:

.. image:: /images/heAvQ15jUu.png

This is the API key you will use to interact with the GPSE.

.. warning::
	An API key is limited to 100 requests per day. When this quota is exceeded,
	:class:`QuotaExceededError` is raised.

Once you have attained this key, you can now use the API:

.. code-block:: python3

	import asyncio
	import cse

	engine = cse.Search("your_api_key")

	async def main():
		results = await engine.search("hello")
		print(results[0].title)

	asyncio.get_event_loop().run_until_complete(main())
