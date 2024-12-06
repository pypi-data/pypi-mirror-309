from typing import Generic, TypeAlias, TypeVar

ErrorCode: TypeAlias = int

_T = TypeVar("_T")
_E = TypeVar("_E")


class Result:
	class Ok(Generic[_T]):
		# private
		def __init__(
			self,
			obj: _T,
			is_constructor_called_privately: bool = False,
		):
			if not is_constructor_called_privately:
				raise Exception("This constructor shall be called privately only.")
			self._obj = obj

		@property
		def obj(self) -> _T:
			return self._obj

		@property
		def is_ok(self) -> bool:
			return True

		@property
		def is_err(self) -> bool:
			return False

	class Err(Generic[_E]):
		# private
		def __init__(
			self,
			obj: _E,
			is_constructor_called_privately: bool = False,
		):
			if not is_constructor_called_privately:
				raise Exception("This constructor shall be called privately only.")
			self._obj = obj

		@property
		def obj(self) -> _E:
			return self._obj

		@property
		def is_ok(self) -> bool:
			return False

		@property
		def is_err(self) -> bool:
			return True

	@staticmethod
	def ok(obj: _T) -> "Result.Ok[_T]":
		return Result.Ok(obj=obj, is_constructor_called_privately=True)

	@staticmethod
	def err(obj: _E) -> "Result.Err[_E]":
		return Result.Err(obj=obj, is_constructor_called_privately=True)

	@staticmethod
	def is_ok(result: "Result.Ok[_T]|Result.Err[_E]") -> bool:
		return result.is_ok

	@staticmethod
	def is_err(result: "Result.Ok[_T]|Result.Err[_E]") -> bool:
		return result.is_err
