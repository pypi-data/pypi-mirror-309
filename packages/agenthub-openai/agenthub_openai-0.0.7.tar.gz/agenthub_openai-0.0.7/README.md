# Agenthub OpenAI Agent

This package contains the OpenAI agent implementation for AgentHub.

## Installation

```bash
pip install agenthub-openai
```

## Usage

```python
from agenthub import Team, Agent

team = Team()

def get_weather(location) -> str:
    return "{'temp':67, 'unit':'F'}"

weather_agent = Agent(
    name="Weather AI",
    instructions="You are a helpful agent.",
    functions=[get_weather],
)

messages = [{"role": "user", "content": "What's the weather in NYC?"}]

response = team.run(agent=weather_agent, messages=messages)
print(response.messages[-1]["content"])
```
