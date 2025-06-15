from state import State


class IdleState(State):
    def mouseDown(self, mousePoint, shiftDown, ctrlDown):
        """Handle mouse down event."""
        pass

    def mouseUp(self, mousePoint, shiftDown, ctrlDown):
        """Handle mouse up event."""
        pass

    def mouseDragged(self, mousePoint):
        """Handle mouse move event."""
        pass

    def keyPressed(self, key):
        """Handle key press event."""
        pass

    def afterDraw(self, renderer, go=None):
        """Handle after object draw or entire canvas draw."""
        pass

    def onLeaving(self):
        """Handle leaving the state."""
        pass