from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    street: str
    number: int
    complement: str
    zip_code: str
    state: str
    country: str

