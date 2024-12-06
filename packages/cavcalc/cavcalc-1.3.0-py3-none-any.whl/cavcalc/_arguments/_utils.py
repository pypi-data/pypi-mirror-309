from dataclasses import dataclass


@dataclass(frozen=True)
class _ReferencedQuantity:
    ref_name: str
