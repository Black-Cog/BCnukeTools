
class BaseAction():
    def __init__( self, window=False, arg={} ):

        self.returnValue = None

        if window:
            self._doUi( arg=arg )
        else:
            self._doAction( arg=arg )

    def _doUi( self, arg ):
        pass

    def _doAction( self, arg ):
        pass
