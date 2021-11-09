from typing import Union

class Light:
    STATES = [
        'red',
        'yellow',
        'green',
    ]

    def __init__(self, name: str='beer30', state: Union[str,int]='red') -> None:
        self._name = name
        self.state = state

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, newname: str) -> None:
        if not isinstance(newname, str):
            raise ValueError('name must be a string')

    @property
    def state(self) -> str:
        return self.STATES[self._value]

    @state.setter
    def state(self, newstate: Union[str,int]) -> None:
        """state sets the Light's state"""
        if isinstance(newstate, int):
            if newstate < 0 or newstate >= len(self.STATES):
                raise ValueError('invalid state integer')
            newvalue = self.STATES.index(newstate)
        elif isinstance(newstate, str):
            if newstate not in self.STATES:
                raise ValueError(f"state '{newstate}' was not found. valid options are: {', '.join(self.STATES)}")
            newvalue = self.STATES.index(newstate)
        else:
            return TypeError('state must be a string or integer')
        self._value = newvalue
