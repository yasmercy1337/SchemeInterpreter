from __future__ import annotations
from dataclasses import dataclass, field
from typing import *
import enum


@dataclass
class ConsList:
    head: Any = None
    next: Any = None
    
    def _last(self) -> Self:
        out = self
        while isinstance(out.next, ConsList):
            out = out.next
        return out
    
    def from_list(arr: list) -> Self:
        if not arr:
            return ConsList()
        head, *next = arr
        if not next:
            return ConsList(head)
        return ConsList(head, ConsList.from_list(next))
        
    def append(self, element: Any) -> None:
        last = self._last()
        if last.head is None:
            last.head = element
            return
        last.next = element
            
    def to_string(self) -> str:
        if self.head is None:
            return ""
        if self.next is None:
            return f"{self.head}"
        if isinstance(self.next, ConsList):
            if self.next.head is not None:
                return f"{self.head} {self.next.to_string()}"
            return f"{self.head}"
        return f"{self.head} . {self.next}"
        
    def __repr__(self) -> str:
        return f"[{self.to_string()}]"
    
    def empty(arr: ConsList) -> bool:
        return arr and arr.head