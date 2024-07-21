from dataclasses import dataclass


@dataclass(eq=False)
class GetUserByIdFilter:
    user_id: int
