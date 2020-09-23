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

import inspect
from enum import Enum
from functools import wraps
from typing import (
	Any,
	Callable,
	Dict,
	Generator,
	List,
	Mapping,
	Optional,
	Tuple,
	Type,
	TypeVar,
	Union
)

__all__ = [
	'Language',
	'CountryCode',
	# 'Geolocation'
]

T = TypeVar('T', bound='BaseFlags')

class _flag_property:
	__slots__ = ('_original_func', '__doc__')

	def __init__(self, func: Union[Callable[[T], bool], Callable[[None], bool]]) -> None:
		self._original_func = func
		self.__doc__ = func.__doc__

	def __get__(self, instance: Optional[T], owner: Optional[Type[T]]=None) -> Union[_flag_property, bool]:
		if instance is None:
			# return super().__get__(instance, owner)
			# raise AttributeError(f'"{self._original_func.__name__}"')
			return self
		return instance._has_flag(self._original_func(None))  # type: ignore

	def __set__(self, instance: T, value: bool) -> None:
		instance._set_flag(self._original_func(None), value) # type: ignore

class BaseFlags:
	__slots__ = ('value',)

	flag_values: List[str]
	value: int

	def __repr__(self) -> str:
		return "<{0.__class__.__name__}: {0.value:#x}>".format(self)

	def __init_subclass__(cls) -> None:
		for name, method in inspect.getmembers(cls):
			if isinstance(method, _flag_property):
				cls.flag_values.append(name)

	def __setattr__(self, name: str, value: Any) -> None:
		if not hasattr(self, name) and name != 'value':
			raise AttributeError(name)
		super(BaseFlags, self).__setattr__(name, value)

	@classmethod
	def _from_value(cls: Type[T], value: int) -> T:
		self = cls()
		self.value = value
		return self 

	def _has_flag(self: T, flag: int) -> bool:
		return (self.value & flag) == flag

	def _set_flag(self: T, flag: int, toggle: bool) -> None:
		if toggle:
			self.value |= flag
		else:
			self.value &= ~flag

	def __iter__(self) -> Generator[Tuple[str, bool], None, None]:
		return ((k, v) for k, v in self.__dict__.items())

	@classmethod
	def all(cls: Type[T]) -> T:
		"""Factory method that returns the flags with all flags enabled."""
		return cls._from_value(int('1'*len(cls.flag_values), 2))

	@classmethod
	def none(cls: Type[T]) -> T:
		"""Factory method that returns the flags with all flags disabled."""
		return cls._from_value(0)

	@classmethod
	def from_flags(cls: Type[T], **flags: Mapping[str, _flag_property]) -> T:
		"""Factory method that returns the flags with specific flags enabled."""
		self = cls._from_value(0)
		for name, value in flags.items():
			if not hasattr(self, name):
				raise AttributeError(name)
			setattr(self, name, value)
		return self

	@property
	def _all_flags_enabled(self: T) -> bool:
		return self.value == (1 << len(self.flag_values)) - 1

	def to_google_flags(self: T) -> Optional[str]:
		"""Converts these flags to a url-safe parameter value."""
		val = bin(self.value)

		if self.value == 0 or self._all_flags_enabled:
			return None

		if val.count('1') > (len(self.flag_values) / 2):
			return '-(' + '|'.join(getattr(self.__class__, k).__doc__ for k, v in self if not v) + ')'
		return '|'.join(getattr(self.__class__, k).__doc__ for k, v in self if v)

class Language(BaseFlags):
	"""
	Bit flags for the ``lr`` and ``cr`` parameters.
	"""
	__slots__ = ('value',)

	flag_values: List[str] = []

	@property
	def __dict__(self) -> Dict[str, Any]:  # type: ignore
		return {name: getattr(self, name) for name in self.flag_values}

	@_flag_property
	def arabic(self) -> bool:
		'lang_ar'
		return 1  # type: ignore

	@_flag_property
	def bulgarian(self) -> bool:
		'lang_bg'
		return 1 << 1  # type: ignore

	@_flag_property
	def catalan(self) -> bool:
		'lang_ca'
		return 1 << 2  # type: ignore

	@_flag_property
	def czech(self) -> bool:
		'lang_cs'
		return 1 << 3  # type: ignore

	@_flag_property
	def danish(self) -> bool:
		'lang_da'
		return 1 << 4  # type: ignore

	@_flag_property
	def german(self) -> bool:
		'lang_de'
		return 1 << 5  # type: ignore

	@_flag_property
	def greek(self) -> bool:
		'lang_el'
		return 1 << 6  # type: ignore

	@_flag_property
	def english(self) -> bool:
		'lang_en'
		return 1 << 7  # type: ignore

	@_flag_property
	def spanish(self) -> bool:
		'lang_es'
		return 1 << 8  # type: ignore

	@_flag_property
	def estonian(self) -> bool:
		'lang_et'
		return 1 << 9  # type: ignore

	@_flag_property
	def finnish(self) -> bool:
		'lang_fi'
		return 1 << 10  # type: ignore

	@_flag_property
	def french(self) -> bool:
		'lang_fr'
		return 1 << 11  # type: ignore

	@_flag_property
	def croatian(self) -> bool:
		'lang_hr'
		return 1 << 12  # type: ignore

	@_flag_property
	def hungarian(self) -> bool:
		'lang_hu'
		return 1 << 13  # type: ignore

	@_flag_property
	def indonesian(self) -> bool:
		'lang_id'
		return 1 << 14  # type: ignore

	@_flag_property
	def icelandic(self) -> bool:
		'lang_is'
		return 1 << 15  # type: ignore

	@_flag_property
	def italian(self) -> bool:
		'lang_it'
		return 1 << 16  # type: ignore

	@_flag_property
	def hebrew(self) -> bool:
		'lang_iw'
		return 1 << 17  # type: ignore

	@_flag_property
	def japanese(self) -> bool:
		'lang_ja'
		return 1 << 18  # type: ignore

	@_flag_property
	def korean(self) -> bool:
		'lang_ko'
		return 1 << 19  # type: ignore

	@_flag_property
	def lithuanian(self) -> bool:
		'lang_lt'
		return 1 << 20  # type: ignore

	@_flag_property
	def latvian(self) -> bool:
		'lang_lv'
		return 1 << 21  # type: ignore

	@_flag_property
	def dutch(self) -> bool:
		'lang_nl'
		return 1 << 22  # type: ignore

	@_flag_property
	def norwegian(self) -> bool:
		'lang_no'
		return 1 << 23  # type: ignore

	@_flag_property
	def polish(self) -> bool:
		'lang_pl'
		return 1 << 24  # type: ignore

	@_flag_property
	def portuguese(self) -> bool:
		'lang_pt'
		return 1 << 25  # type: ignore

	@_flag_property
	def romanian(self) -> bool:
		'lang_ro'
		return 1 << 26  # type: ignore

	@_flag_property
	def russian(self) -> bool:
		'lang_ru'
		return 1 << 27  # type: ignore

	@_flag_property
	def slovak(self) -> bool:
		'lang_sk'
		return 1 << 28  # type: ignore

	@_flag_property
	def slovenian(self) -> bool:
		'lang_sl'
		return 1 << 29  # type: ignore

	@_flag_property
	def serbian(self) -> bool:
		'lang_sr'
		return 1 << 30  # type: ignore

	@_flag_property
	def swedish(self) -> bool:
		'lang_sv'
		return 1 << 31  # type: ignore

	@_flag_property
	def turkish(self) -> bool:
		'lang_tr'
		return 1 << 32  # type: ignore

	@_flag_property
	def chinese_simplified(self) -> bool:
		'lang_zh-CN'
		return 1 << 33  # type: ignore

	@_flag_property
	def chinese_traditional(self) -> bool:
		'lang_zh-TW'
		return 1 << 34  # type: ignore

class CountryCode(BaseFlags):
	__slots__ = ('value',)

	flag_values: List[str] = []

	@property
	def __dict__(self) -> Dict[str, Any]:  # type: ignore
		return {name: getattr(self, name) for name in self.flag_values}

	@_flag_property
	def afghanistan(self) -> bool:
		'countryAF'
		return 1 << 0  # type: ignore

	@_flag_property
	def albania(self) -> bool:
		'countryAL'
		return 1 << 1  # type: ignore

	@_flag_property
	def algeria(self) -> bool:
		'countryDZ'
		return 1 << 2  # type: ignore

	@_flag_property
	def american_samoa(self) -> bool:
		'countryAS'
		return 1 << 3  # type: ignore

	@_flag_property
	def andorra(self) -> bool:
		'countryAD'
		return 1 << 4  # type: ignore

	@_flag_property
	def angola(self) -> bool:
		'countryAO'
		return 1 << 5  # type: ignore

	@_flag_property
	def anguilla(self) -> bool:
		'countryAI'
		return 1 << 6  # type: ignore

	@_flag_property
	def antarctica(self) -> bool:
		'countryAQ'
		return 1 << 7  # type: ignore

	@_flag_property
	def antigua_and_barbuda(self) -> bool:
		'countryAG'
		return 1 << 8  # type: ignore

	@_flag_property
	def argentina(self) -> bool:
		'countryAR'
		return 1 << 9  # type: ignore

	@_flag_property
	def armenia(self) -> bool:
		'countryAM'
		return 1 << 10  # type: ignore

	@_flag_property
	def aruba(self) -> bool:
		'countryAW'
		return 1 << 11  # type: ignore

	@_flag_property
	def australia(self) -> bool:
		'countryAU'
		return 1 << 12  # type: ignore

	@_flag_property
	def austria(self) -> bool:
		'countryAT'
		return 1 << 13  # type: ignore

	@_flag_property
	def azerbaijan(self) -> bool:
		'countryAZ'
		return 1 << 14  # type: ignore

	@_flag_property
	def bahamas(self) -> bool:
		'countryBS'
		return 1 << 15  # type: ignore

	@_flag_property
	def bahrain(self) -> bool:
		'countryBH'
		return 1 << 16  # type: ignore

	@_flag_property
	def bangladesh(self) -> bool:
		'countryBD'
		return 1 << 17  # type: ignore

	@_flag_property
	def barbados(self) -> bool:
		'countryBB'
		return 1 << 18  # type: ignore

	@_flag_property
	def belarus(self) -> bool:
		'countryBY'
		return 1 << 19  # type: ignore

	@_flag_property
	def belgium(self) -> bool:
		'countryBE'
		return 1 << 20  # type: ignore

	@_flag_property
	def belize(self) -> bool:
		'countryBZ'
		return 1 << 21  # type: ignore

	@_flag_property
	def benin(self) -> bool:
		'countryBJ'
		return 1 << 22  # type: ignore

	@_flag_property
	def bermuda(self) -> bool:
		'countryBM'
		return 1 << 23  # type: ignore

	@_flag_property
	def bhutan(self) -> bool:
		'countryBT'
		return 1 << 24  # type: ignore

	@_flag_property
	def bolivia(self) -> bool:
		'countryBO'
		return 1 << 25  # type: ignore

	@_flag_property
	def bosnia_and_herzegovina(self) -> bool:
		'countryBA'
		return 1 << 26  # type: ignore

	@_flag_property
	def botswana(self) -> bool:
		'countryBW'
		return 1 << 27  # type: ignore

	@_flag_property
	def bouvet_island(self) -> bool:
		'countryBV'
		return 1 << 28  # type: ignore

	@_flag_property
	def brazil(self) -> bool:
		'countryBR'
		return 1 << 29  # type: ignore

	@_flag_property
	def british_indian_ocean_territory(self) -> bool:
		'countryIO'
		return 1 << 30  # type: ignore

	@_flag_property
	def brunei_darussalam(self) -> bool:
		'countryBN'
		return 1 << 31  # type: ignore

	@_flag_property
	def bulgaria(self) -> bool:
		'countryBG'
		return 1 << 32  # type: ignore

	@_flag_property
	def burkina_faso(self) -> bool:
		'countryBF'
		return 1 << 33  # type: ignore

	@_flag_property
	def burundi(self) -> bool:
		'countryBI'
		return 1 << 34  # type: ignore

	@_flag_property
	def cambodia(self) -> bool:
		'countryKH'
		return 1 << 35  # type: ignore

	@_flag_property
	def cameroon(self) -> bool:
		'countryCM'
		return 1 << 36  # type: ignore

	@_flag_property
	def canada(self) -> bool:
		'countryCA'
		return 1 << 37  # type: ignore

	@_flag_property
	def cape_verde(self) -> bool:
		'countryCV'
		return 1 << 38  # type: ignore

	@_flag_property
	def cayman_islands(self) -> bool:
		'countryKY'
		return 1 << 39  # type: ignore

	@_flag_property
	def central_african_republic(self) -> bool:
		'countryCF'
		return 1 << 40  # type: ignore

	@_flag_property
	def chad(self) -> bool:
		'countryTD'
		return 1 << 41  # type: ignore

	@_flag_property
	def chile(self) -> bool:
		'countryCL'
		return 1 << 42  # type: ignore

	@_flag_property
	def china(self) -> bool:
		'countryCN'
		return 1 << 43  # type: ignore

	@_flag_property
	def christmas_island(self) -> bool:
		'countryCX'
		return 1 << 44  # type: ignore

	@_flag_property
	def cocos_keeling_islands(self) -> bool:
		'countryCC'
		return 1 << 45  # type: ignore

	@_flag_property
	def colombia(self) -> bool:
		'countryCO'
		return 1 << 46  # type: ignore

	@_flag_property
	def comoros(self) -> bool:
		'countryKM'
		return 1 << 47  # type: ignore

	@_flag_property
	def congo(self) -> bool:
		'countryCG'
		return 1 << 48  # type: ignore

	@_flag_property
	def _the_democratic_republic_of_the_congo(self) -> bool:
		'countryCD'
		return 1 << 49  # type: ignore

	@_flag_property
	def cook_islands(self) -> bool:
		'countryCK'
		return 1 << 50  # type: ignore

	@_flag_property
	def costa_rica(self) -> bool:
		'countryCR'
		return 1 << 51  # type: ignore

	@_flag_property
	def cote_divoire(self) -> bool:
		'countryCI'
		return 1 << 52  # type: ignore

	@_flag_property
	def croatia_hrvatska(self) -> bool:
		'countryHR'
		return 1 << 53  # type: ignore

	@_flag_property
	def cuba(self) -> bool:
		'countryCU'
		return 1 << 54  # type: ignore

	@_flag_property
	def cyprus(self) -> bool:
		'countryCY'
		return 1 << 55  # type: ignore

	@_flag_property
	def czech_republic(self) -> bool:
		'countryCZ'
		return 1 << 56  # type: ignore

	@_flag_property
	def denmark(self) -> bool:
		'countryDK'
		return 1 << 57  # type: ignore

	@_flag_property
	def djibouti(self) -> bool:
		'countryDJ'
		return 1 << 58  # type: ignore

	@_flag_property
	def dominica(self) -> bool:
		'countryDM'
		return 1 << 59  # type: ignore

	@_flag_property
	def dominican_republic(self) -> bool:
		'countryDO'
		return 1 << 60  # type: ignore

	@_flag_property
	def east_timor(self) -> bool:
		'countryTP'
		return 1 << 61  # type: ignore

	@_flag_property
	def ecuador(self) -> bool:
		'countryEC'
		return 1 << 62  # type: ignore

	@_flag_property
	def egypt(self) -> bool:
		'countryEG'
		return 1 << 63  # type: ignore

	@_flag_property
	def el_salvador(self) -> bool:
		'countrySV'
		return 1 << 64  # type: ignore

	@_flag_property
	def equatorial_guinea(self) -> bool:
		'countryGQ'
		return 1 << 65  # type: ignore

	@_flag_property
	def eritrea(self) -> bool:
		'countryER'
		return 1 << 66  # type: ignore

	@_flag_property
	def estonia(self) -> bool:
		'countryEE'
		return 1 << 67  # type: ignore

	@_flag_property
	def ethiopia(self) -> bool:
		'countryET'
		return 1 << 68  # type: ignore

	@_flag_property
	def european_union(self) -> bool:
		'countryEU'
		return 1 << 69  # type: ignore

	@_flag_property
	def falkland_islands_malvinas(self) -> bool:
		'countryFK'
		return 1 << 70  # type: ignore

	@_flag_property
	def faroe_islands(self) -> bool:
		'countryFO'
		return 1 << 71  # type: ignore

	@_flag_property
	def fiji(self) -> bool:
		'countryFJ'
		return 1 << 72  # type: ignore

	@_flag_property
	def finland(self) -> bool:
		'countryFI'
		return 1 << 73  # type: ignore

	@_flag_property
	def france(self) -> bool:
		'countryFR'
		return 1 << 74  # type: ignore

	@_flag_property
	def _metropolitan_france(self) -> bool:
		'countryFX'
		return 1 << 75  # type: ignore

	@_flag_property
	def french_guiana(self) -> bool:
		'countryGF'
		return 1 << 76  # type: ignore

	@_flag_property
	def french_polynesia(self) -> bool:
		'countryPF'
		return 1 << 77  # type: ignore

	@_flag_property
	def french_southern_territories(self) -> bool:
		'countryTF'
		return 1 << 78  # type: ignore

	@_flag_property
	def gabon(self) -> bool:
		'countryGA'
		return 1 << 79  # type: ignore

	@_flag_property
	def gambia(self) -> bool:
		'countryGM'
		return 1 << 80  # type: ignore

	@_flag_property
	def georgia(self) -> bool:
		'countryGE'
		return 1 << 81  # type: ignore

	@_flag_property
	def germany(self) -> bool:
		'countryDE'
		return 1 << 82  # type: ignore

	@_flag_property
	def ghana(self) -> bool:
		'countryGH'
		return 1 << 83  # type: ignore

	@_flag_property
	def gibraltar(self) -> bool:
		'countryGI'
		return 1 << 84  # type: ignore

	@_flag_property
	def greece(self) -> bool:
		'countryGR'
		return 1 << 85  # type: ignore

	@_flag_property
	def greenland(self) -> bool:
		'countryGL'
		return 1 << 86  # type: ignore

	@_flag_property
	def grenada(self) -> bool:
		'countryGD'
		return 1 << 87  # type: ignore

	@_flag_property
	def guadeloupe(self) -> bool:
		'countryGP'
		return 1 << 88  # type: ignore

	@_flag_property
	def guam(self) -> bool:
		'countryGU'
		return 1 << 89  # type: ignore

	@_flag_property
	def guatemala(self) -> bool:
		'countryGT'
		return 1 << 90  # type: ignore

	@_flag_property
	def guinea(self) -> bool:
		'countryGN'
		return 1 << 91  # type: ignore

	@_flag_property
	def guinea_bissau(self) -> bool:
		'countryGW'
		return 1 << 92  # type: ignore

	@_flag_property
	def guyana(self) -> bool:
		'countryGY'
		return 1 << 93  # type: ignore

	@_flag_property
	def haiti(self) -> bool:
		'countryHT'
		return 1 << 94  # type: ignore

	@_flag_property
	def heard_island_and_mcdonald_islands(self) -> bool:
		'countryHM'
		return 1 << 95  # type: ignore

	@_flag_property
	def holy_see_vatican_city_state(self) -> bool:
		'countryVA'
		return 1 << 96  # type: ignore

	@_flag_property
	def honduras(self) -> bool:
		'countryHN'
		return 1 << 97  # type: ignore

	@_flag_property
	def hong_kong(self) -> bool:
		'countryHK'
		return 1 << 98  # type: ignore

	@_flag_property
	def hungary(self) -> bool:
		'countryHU'
		return 1 << 99  # type: ignore

	@_flag_property
	def iceland(self) -> bool:
		'countryIS'
		return 1 << 100  # type: ignore

	@_flag_property
	def india(self) -> bool:
		'countryIN'
		return 1 << 101  # type: ignore

	@_flag_property
	def indonesia(self) -> bool:
		'countryID'
		return 1 << 102  # type: ignore

	@_flag_property
	def _islamic_republic_of_iran(self) -> bool:
		'countryIR'
		return 1 << 103  # type: ignore

	@_flag_property
	def iraq(self) -> bool:
		'countryIQ'
		return 1 << 104  # type: ignore

	@_flag_property
	def ireland(self) -> bool:
		'countryIE'
		return 1 << 105  # type: ignore

	@_flag_property
	def israel(self) -> bool:
		'countryIL'
		return 1 << 106  # type: ignore

	@_flag_property
	def italy(self) -> bool:
		'countryIT'
		return 1 << 107  # type: ignore

	@_flag_property
	def jamaica(self) -> bool:
		'countryJM'
		return 1 << 108  # type: ignore

	@_flag_property
	def japan(self) -> bool:
		'countryJP'
		return 1 << 109  # type: ignore

	@_flag_property
	def jordan(self) -> bool:
		'countryJO'
		return 1 << 110  # type: ignore

	@_flag_property
	def kazakhstan(self) -> bool:
		'countryKZ'
		return 1 << 111  # type: ignore

	@_flag_property
	def kenya(self) -> bool:
		'countryKE'
		return 1 << 112  # type: ignore

	@_flag_property
	def kiribati(self) -> bool:
		'countryKI'
		return 1 << 113  # type: ignore

	@_flag_property
	def _democratic_peoples_republic_of_korea(self) -> bool:
		'countryKP'
		return 1 << 114  # type: ignore

	@_flag_property
	def _republic_of_korea(self) -> bool:
		'countryKR'
		return 1 << 115  # type: ignore

	@_flag_property
	def kuwait(self) -> bool:
		'countryKW'
		return 1 << 116  # type: ignore

	@_flag_property
	def kyrgyzstan(self) -> bool:
		'countryKG'
		return 1 << 117  # type: ignore

	@_flag_property
	def lao_peoples_democratic_republic(self) -> bool:
		'countryLA'
		return 1 << 118  # type: ignore

	@_flag_property
	def latvia(self) -> bool:
		'countryLV'
		return 1 << 119  # type: ignore

	@_flag_property
	def lebanon(self) -> bool:
		'countryLB'
		return 1 << 120  # type: ignore

	@_flag_property
	def lesotho(self) -> bool:
		'countryLS'
		return 1 << 121  # type: ignore

	@_flag_property
	def liberia(self) -> bool:
		'countryLR'
		return 1 << 122  # type: ignore

	@_flag_property
	def libyan_arab_jamahiriya(self) -> bool:
		'countryLY'
		return 1 << 123  # type: ignore

	@_flag_property
	def liechtenstein(self) -> bool:
		'countryLI'
		return 1 << 124  # type: ignore

	@_flag_property
	def lithuania(self) -> bool:
		'countryLT'
		return 1 << 125  # type: ignore

	@_flag_property
	def luxembourg(self) -> bool:
		'countryLU'
		return 1 << 126  # type: ignore

	@_flag_property
	def macao(self) -> bool:
		'countryMO'
		return 1 << 127  # type: ignore

	@_flag_property
	def _the_former_yugosalv_republic_of_macedonia(self) -> bool:
		'countryMK'
		return 1 << 128  # type: ignore

	@_flag_property
	def madagascar(self) -> bool:
		'countryMG'
		return 1 << 129  # type: ignore

	@_flag_property
	def malawi(self) -> bool:
		'countryMW'
		return 1 << 130  # type: ignore

	@_flag_property
	def malaysia(self) -> bool:
		'countryMY'
		return 1 << 131  # type: ignore

	@_flag_property
	def maldives(self) -> bool:
		'countryMV'
		return 1 << 132  # type: ignore

	@_flag_property
	def mali(self) -> bool:
		'countryML'
		return 1 << 133  # type: ignore

	@_flag_property
	def malta(self) -> bool:
		'countryMT'
		return 1 << 134  # type: ignore

	@_flag_property
	def marshall_islands(self) -> bool:
		'countryMH'
		return 1 << 135  # type: ignore

	@_flag_property
	def martinique(self) -> bool:
		'countryMQ'
		return 1 << 136  # type: ignore

	@_flag_property
	def mauritania(self) -> bool:
		'countryMR'
		return 1 << 137  # type: ignore

	@_flag_property
	def mauritius(self) -> bool:
		'countryMU'
		return 1 << 138  # type: ignore

	@_flag_property
	def mayotte(self) -> bool:
		'countryYT'
		return 1 << 139  # type: ignore

	@_flag_property
	def mexico(self) -> bool:
		'countryMX'
		return 1 << 140  # type: ignore

	@_flag_property
	def _federated_states_of_micronesia(self) -> bool:
		'countryFM'
		return 1 << 141  # type: ignore

	@_flag_property
	def _republic_of_moldova(self) -> bool:
		'countryMD'
		return 1 << 142  # type: ignore

	@_flag_property
	def monaco(self) -> bool:
		'countryMC'
		return 1 << 143  # type: ignore

	@_flag_property
	def mongolia(self) -> bool:
		'countryMN'
		return 1 << 144  # type: ignore

	@_flag_property
	def montserrat(self) -> bool:
		'countryMS'
		return 1 << 145  # type: ignore

	@_flag_property
	def morocco(self) -> bool:
		'countryMA'
		return 1 << 146  # type: ignore

	@_flag_property
	def mozambique(self) -> bool:
		'countryMZ'
		return 1 << 147  # type: ignore

	@_flag_property
	def myanmar(self) -> bool:
		'countryMM'
		return 1 << 148  # type: ignore

	@_flag_property
	def namibia(self) -> bool:
		'countryNA'
		return 1 << 149  # type: ignore

	@_flag_property
	def nauru(self) -> bool:
		'countryNR'
		return 1 << 150  # type: ignore

	@_flag_property
	def nepal(self) -> bool:
		'countryNP'
		return 1 << 151  # type: ignore

	@_flag_property
	def netherlands(self) -> bool:
		'countryNL'
		return 1 << 152  # type: ignore

	@_flag_property
	def netherlands_antilles(self) -> bool:
		'countryAN'
		return 1 << 153  # type: ignore

	@_flag_property
	def new_caledonia(self) -> bool:
		'countryNC'
		return 1 << 154  # type: ignore

	@_flag_property
	def new_zealand(self) -> bool:
		'countryNZ'
		return 1 << 155  # type: ignore

	@_flag_property
	def nicaragua(self) -> bool:
		'countryNI'
		return 1 << 156  # type: ignore

	@_flag_property
	def niger(self) -> bool:
		'countryNE'
		return 1 << 157  # type: ignore

	@_flag_property
	def nigeria(self) -> bool:
		'countryNG'
		return 1 << 158  # type: ignore

	@_flag_property
	def niue(self) -> bool:
		'countryNU'
		return 1 << 159  # type: ignore

	@_flag_property
	def norfolk_island(self) -> bool:
		'countryNF'
		return 1 << 160  # type: ignore

	@_flag_property
	def northern_mariana_islands(self) -> bool:
		'countryMP'
		return 1 << 161  # type: ignore

	@_flag_property
	def norway(self) -> bool:
		'countryNO'
		return 1 << 162  # type: ignore

	@_flag_property
	def oman(self) -> bool:
		'countryOM'
		return 1 << 163  # type: ignore

	@_flag_property
	def pakistan(self) -> bool:
		'countryPK'
		return 1 << 164  # type: ignore

	@_flag_property
	def palau(self) -> bool:
		'countryPW'
		return 1 << 165  # type: ignore

	@_flag_property
	def palestinian_territory(self) -> bool:
		'countryPS'
		return 1 << 166  # type: ignore

	@_flag_property
	def panama(self) -> bool:
		'countryPA'
		return 1 << 167  # type: ignore

	@_flag_property
	def papua_new_guinea(self) -> bool:
		'countryPG'
		return 1 << 168  # type: ignore

	@_flag_property
	def paraguay(self) -> bool:
		'countryPY'
		return 1 << 169  # type: ignore

	@_flag_property
	def peru(self) -> bool:
		'countryPE'
		return 1 << 170  # type: ignore

	@_flag_property
	def philippines(self) -> bool:
		'countryPH'
		return 1 << 171  # type: ignore

	@_flag_property
	def pitcairn(self) -> bool:
		'countryPN'
		return 1 << 172  # type: ignore

	@_flag_property
	def poland(self) -> bool:
		'countryPL'
		return 1 << 173  # type: ignore

	@_flag_property
	def portugal(self) -> bool:
		'countryPT'
		return 1 << 174  # type: ignore

	@_flag_property
	def puerto_rico(self) -> bool:
		'countryPR'
		return 1 << 175  # type: ignore

	@_flag_property
	def qatar(self) -> bool:
		'countryQA'
		return 1 << 176  # type: ignore

	@_flag_property
	def reunion(self) -> bool:
		'countryRE'
		return 1 << 177  # type: ignore

	@_flag_property
	def romania(self) -> bool:
		'countryRO'
		return 1 << 178  # type: ignore

	@_flag_property
	def russian_federation(self) -> bool:
		'countryRU'
		return 1 << 179  # type: ignore

	@_flag_property
	def rwanda(self) -> bool:
		'countryRW'
		return 1 << 180  # type: ignore

	@_flag_property
	def saint_helena(self) -> bool:
		'countrySH'
		return 1 << 181  # type: ignore

	@_flag_property
	def saint_kitts_and_nevis(self) -> bool:
		'countryKN'
		return 1 << 182  # type: ignore

	@_flag_property
	def saint_lucia(self) -> bool:
		'countryLC'
		return 1 << 183  # type: ignore

	@_flag_property
	def saint_pierre_and_miquelon(self) -> bool:
		'countryPM'
		return 1 << 184  # type: ignore

	@_flag_property
	def saint_vincent_and_the_grenadines(self) -> bool:
		'countryVC'
		return 1 << 185  # type: ignore

	@_flag_property
	def samoa(self) -> bool:
		'countryWS'
		return 1 << 186  # type: ignore

	@_flag_property
	def san_marino(self) -> bool:
		'countrySM'
		return 1 << 187  # type: ignore

	@_flag_property
	def sao_tome_and_principe(self) -> bool:
		'countryST'
		return 1 << 188  # type: ignore

	@_flag_property
	def saudi_arabia(self) -> bool:
		'countrySA'
		return 1 << 189  # type: ignore

	@_flag_property
	def senegal(self) -> bool:
		'countrySN'
		return 1 << 190  # type: ignore

	@_flag_property
	def serbia_and_montenegro(self) -> bool:
		'countryCS'
		return 1 << 191  # type: ignore

	@_flag_property
	def seychelles(self) -> bool:
		'countrySC'
		return 1 << 192  # type: ignore

	@_flag_property
	def sierra_leone(self) -> bool:
		'countrySL'
		return 1 << 193  # type: ignore

	@_flag_property
	def singapore(self) -> bool:
		'countrySG'
		return 1 << 194  # type: ignore

	@_flag_property
	def slovakia(self) -> bool:
		'countrySK'
		return 1 << 195  # type: ignore

	@_flag_property
	def slovenia(self) -> bool:
		'countrySI'
		return 1 << 196  # type: ignore

	@_flag_property
	def solomon_islands(self) -> bool:
		'countrySB'
		return 1 << 197  # type: ignore

	@_flag_property
	def somalia(self) -> bool:
		'countrySO'
		return 1 << 198  # type: ignore

	@_flag_property
	def south_africa(self) -> bool:
		'countryZA'
		return 1 << 199  # type: ignore

	@_flag_property
	def south_georgia_and_the_south_sandwich_islands(self) -> bool:
		'countryGS'
		return 1 << 200  # type: ignore

	@_flag_property
	def spain(self) -> bool:
		'countryES'
		return 1 << 201  # type: ignore

	@_flag_property
	def sri_lanka(self) -> bool:
		'countryLK'
		return 1 << 202  # type: ignore

	@_flag_property
	def sudan(self) -> bool:
		'countrySD'
		return 1 << 203  # type: ignore

	@_flag_property
	def suriname(self) -> bool:
		'countrySR'
		return 1 << 204  # type: ignore

	@_flag_property
	def svalbard_and_jan_mayen(self) -> bool:
		'countrySJ'
		return 1 << 205  # type: ignore

	@_flag_property
	def swaziland(self) -> bool:
		'countrySZ'
		return 1 << 206  # type: ignore

	@_flag_property
	def sweden(self) -> bool:
		'countrySE'
		return 1 << 207  # type: ignore

	@_flag_property
	def switzerland(self) -> bool:
		'countryCH'
		return 1 << 208  # type: ignore

	@_flag_property
	def syrian_arab_republic(self) -> bool:
		'countrySY'
		return 1 << 209  # type: ignore

	@_flag_property
	def _province_of_china_taiwan(self) -> bool:
		'countryTW'
		return 1 << 210  # type: ignore

	@_flag_property
	def tajikistan(self) -> bool:
		'countryTJ'
		return 1 << 211  # type: ignore

	@_flag_property
	def _united_republic_of_tanzania(self) -> bool:
		'countryTZ'
		return 1 << 212  # type: ignore

	@_flag_property
	def thailand(self) -> bool:
		'countryTH'
		return 1 << 213  # type: ignore

	@_flag_property
	def togo(self) -> bool:
		'countryTG'
		return 1 << 214  # type: ignore

	@_flag_property
	def tokelau(self) -> bool:
		'countryTK'
		return 1 << 215  # type: ignore

	@_flag_property
	def tonga(self) -> bool:
		'countryTO'
		return 1 << 216  # type: ignore

	@_flag_property
	def trinidad_and_tobago(self) -> bool:
		'countryTT'
		return 1 << 217  # type: ignore

	@_flag_property
	def tunisia(self) -> bool:
		'countryTN'
		return 1 << 218  # type: ignore

	@_flag_property
	def turkey(self) -> bool:
		'countryTR'
		return 1 << 219  # type: ignore

	@_flag_property
	def turkmenistan(self) -> bool:
		'countryTM'
		return 1 << 220  # type: ignore

	@_flag_property
	def turks_and_caicos_islands(self) -> bool:
		'countryTC'
		return 1 << 221  # type: ignore

	@_flag_property
	def tuvalu(self) -> bool:
		'countryTV'
		return 1 << 222  # type: ignore

	@_flag_property
	def uganda(self) -> bool:
		'countryUG'
		return 1 << 223  # type: ignore

	@_flag_property
	def ukraine(self) -> bool:
		'countryUA'
		return 1 << 224  # type: ignore

	@_flag_property
	def united_arab_emirates(self) -> bool:
		'countryAE'
		return 1 << 225  # type: ignore

	@_flag_property
	def united_kingdom(self) -> bool:
		'countryUK'
		return 1 << 226  # type: ignore

	@_flag_property
	def united_states(self) -> bool:
		'countryUS'
		return 1 << 227  # type: ignore

	@_flag_property
	def united_states_minor_outlying_islands(self) -> bool:
		'countryUM'
		return 1 << 228  # type: ignore

	@_flag_property
	def uruguay(self) -> bool:
		'countryUY'
		return 1 << 229  # type: ignore

	@_flag_property
	def uzbekistan(self) -> bool:
		'countryUZ'
		return 1 << 230  # type: ignore

	@_flag_property
	def vanuatu(self) -> bool:
		'countryVU'
		return 1 << 231  # type: ignore

	@_flag_property
	def venezuela(self) -> bool:
		'countryVE'
		return 1 << 232  # type: ignore

	@_flag_property
	def vietnam(self) -> bool:
		'countryVN'
		return 1 << 233  # type: ignore

	@_flag_property
	def _british_virgin_islands(self) -> bool:
		'countryVG'
		return 1 << 234  # type: ignore

	@_flag_property
	def _us_virgin_islands(self) -> bool:
		'countryVI'
		return 1 << 235  # type: ignore

	@_flag_property
	def wallis_and_futuna(self) -> bool:
		'countryWF'
		return 1 << 236  # type: ignore

	@_flag_property
	def western_sahara(self) -> bool:
		'countryEH'
		return 1 << 237  # type: ignore

	@_flag_property
	def yemen(self) -> bool:
		'countryYE'
		return 1 << 238  # type: ignore

	@_flag_property
	def yugoslavia(self) -> bool:
		'countryYU'
		return 1 << 239  # type: ignore

	@_flag_property
	def zambia(self) -> bool:
		'countryZM'
		return 1 << 240  # type: ignore

	@_flag_property
	def zimbabwe(self) -> bool:
		'countryZW'
		return 1 << 241  # type: ignore

