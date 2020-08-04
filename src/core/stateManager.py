class StateManager:
    qualifierPtr = []
    state = {}

    def overrideStates(self, state_override):
        self.state = self._overrideStates(self.state, state_override)

    def _overrideStates(self, state, state_override):
        for key, value in state_override:
            if isinstance(value, object):
                if key not in state:
                    state[key] = {}
                state[key] = _overrideStates(state[key], value)
            else:
                state[key] = value
        return state

    def intializeState(self, initialState = {}):
        self.state = initialState

    def setQualifierPtr(self, qualifiers):
        self.qualifierPtr = qualifiers

    def getState(self, location, default=None):
        qualifiers = location.split('.')
        return self._getState(self.state, qualifiers, default)

    def addState(self, state):
        self.setState(state)

    def setState(self, location, value):
        qualifiers = location.split('.')
        state = self._setState(self.state, qualifiers, value)

    def _getState(self, state, qualifiers, default = None):
        if qualifiers[0] in state:
            if len(qualifiers) == 1:
                return state[qualifiers[0]]
            else:
                return self._getState(state[qualifiers[0]], qualifiers[1:], default)
        else:
            return default

    def _setState(self, state, qualifiers, value):
        if len(qualifiers) == 1:
            state[qualifiers[0]] = value
        else:
            if qualifiers[0] in state:
                state[qualifiers[0]] = self._setState(state[qualifiers[0]],
                                                      qualifiers[1:], value)
            else:
                state[qualifiers[0]] = self._setState({}, qualifiers[1:], value)
        return state

