from dataclasses import dataclass


@dataclass(eq=False)
class GetUserByTokenFilter:
    token: str
