class ThermostatAgent:
    """Reflex agent with short-term memory (hysteresis)."""

    def __init__(self):
        self.open_range = (70.0, 74.0)
        self.closed_range = (63.0, 81.0)
        self.current_mode = "off"  # internal state

    def perceive(self, temperature, store_open):
        # Packs the signals from the environment into an observation.
        return {"temperature": temperature,
                "store_open": store_open}

    def decide(self, obs):
        # Decision policy: rules + internal state.
        if obs["store_open"]:
            low, high = self.open_range
        else:
            low, high = self.closed_range
        middle = (low + high) / 2
        t = obs["temperature"]

        if t < low:
            return "heat"
        if t > high:
            return "cool"
        # In range: keep the current mode until it reaches the middle.
        if self.current_mode == "heat" and t < middle:
            return "heat"
        if self.current_mode == "cool" and t > middle:
            return "cool"
        return "off"

    def act(self, mode):
        # Actuator: here we only store the mode; in real life,
        # we would send a command to the unit.
        self.current_mode = mode
