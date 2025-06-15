from abc import ABC, abstractmethod
from point import Point
from renderer import Renderer
from graphical_object import GraphicalObject

class State(ABC):
    @abstractmethod
    def mouseDown(mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        """Handle mouse down event."""
        pass
    @abstractmethod
    def mouseUp(mousePoint: Point, shiftDown: bool, ctrlDown: bool) -> None:
        """Handle mouse up event."""
        pass
    @abstractmethod
    def mouseDragged(mousePoint: Point) -> None:
        """Handle mouse move event."""
        pass
    @abstractmethod
    def keyPressed(key: str) -> None:
        """Handle key press event."""
        pass
    @abstractmethod
    def afterDraw(renderer: Renderer, go: GraphicalObject) -> None:
        """Handle after object draw."""
        pass
    @abstractmethod
    def onLeaving() -> None:
        """Handle leaving the state."""
        pass