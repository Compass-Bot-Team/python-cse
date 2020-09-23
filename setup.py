import setuptools

with open("requirements.txt") as f:
	requirements = f.read().splitlines()

version = '1.0.0'

with open("README.md") as f:
	readme = f.read()

setuptools.setup(
	name='python-cse',
	author='XuaTheGrate',
	url='https://github.com/XuaTheGrate/python-cse',
	project_urls={
		'Issue Tracker': 'https://github.com/XuaTheGrate/python-cse/issues'
	},
	version=version,
	packages=['cse'],
	license='Apache-2.0',
	description='A Python wrapper for the Google Programmable Search Engine JSON API.',
	long_description=readme,
	long_description_content_type='text/markdown',
	include_package_data=True,
	install_requires=requirements,
	python_requires='>=3.7.4',
	classifiers=[
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: Apache Software License",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Topic :: Internet",
		"Topic :: Software Development :: Libraries",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Utilities"
	]
)
