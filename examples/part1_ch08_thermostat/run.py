from agent import ThermostatAgent

readings = [
    (66.0, True), (69.0, True), (71.0, True), (72.5, True),
    (75.0, True), (73.0, True), (71.5, True), (75.0, False),
]

agent = ThermostatAgent()

for temperature, is_open in readings:
    obs = agent.perceive(temperature, is_open)  # observe
    mode = agent.decide(obs)                    # decide
    agent.act(mode)                             # act
    status = "open" if is_open else "closed"
    print(f"{temperature:4.1f} °F, store {status}: {mode}")
