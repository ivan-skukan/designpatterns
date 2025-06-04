from abc import ABC, abstractmethod

class ClipboardObserver(ABC):
  @abstractmethod
  def updateClipboard(self):
    pass

class ClipboardStack:
  def __init__(self):
    self._stack = []
    self._observers = []

  def push(self, text: str):
    self._stack.append(text)
    self._notify_observers()

  def pop(self) -> str | None:
    if not self._stack:
      return None
    text = self._stack.pop()
    self._notify_observers()
    return text

  def peek(self) -> str | None:
    return self._stack[-1] if self._stack else None

  def is_empty(self) -> bool:
    return not self._stack

  def clear(self):
    self._stack.clear()
    self._notify_observers()

  # no checking. change?
  def add_observer(self, observer: ClipboardObserver):
    self._observers.append(observer)

  def remove_observer(self, observer: ClipboardObserver):
    self._observers.remove(observer)

  def _notify_observers(self):
    for obs in self._observers:
      obs.updateClipboard()
