import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent


greeting_agent = Agent(
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. " "Do not engage in any other conversation or tasks.",
    # Crucial for delegation: Clear description of capability
    description="Handles simple greetings and hellos",
            
 )

farewell_agent = Agent(
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                "Do not perform any other actions.",
    # Crucial for delegation: Clear description of capability
    description="Handles simple farewells and goodbyes",
            
 )


mock_weather_db = {
        "beijing": {"status": "success", "report": "The weather in Beijing is sunny with a temperature of 22°C."},
        "shanghai": {"status": "success", "report": "It's cloudy in Shanghai with a temperature of 24°C."},
        "guangzhou": {"status": "success", "report": "Guangzhou is experiencing light rain and a temperature of 27°C."},
        "chengdu": {"status": "success", "report": "It's overcast in Chengdu with a temperature of 20°C."},
        "shenzhen": {"status": "success", "report": "The weather in Shenzhen is sunny with a temperature of 28°C."},
        "wuhan": {"status": "success", "report": "It's partly cloudy in Wuhan with a temperature of 23°C."},
        "hangzhou": {"status": "success", "report": "Hangzhou is experiencing light drizzle and a temperature of 21°C."},
 }

def get_weather(city: str) -> dict:

    # Best Practice: Log tool execution for easier debugging
    print(f"--- Tool: get_weather called for city: {city} ---")

    mock_weather_db = {
        "beijing": {"status": "success", "report": "The weather in Beijing is sunny with a temperature of 22°C."},
        "shanghai": {"status": "success", "report": "It's cloudy in Shanghai with a temperature of 24°C."},
        "guangzhou": {"status": "success", "report": "Guangzhou is experiencing light rain and a temperature of 27°C."},
        "chengdu": {"status": "success", "report": "It's overcast in Chengdu with a temperature of 20°C."},
        "shenzhen": {"status": "success", "report": "The weather in Shenzhen is sunny with a temperature of 28°C."},
        "wuhan": {"status": "success", "report": "It's partly cloudy in Wuhan with a temperature of 23°C."},
        "hangzhou": {"status": "success", "report": "Hangzhou is experiencing light drizzle and a temperature of 21°C."},
 }
    city_normalized = city.lower().replace(" ", "") # Basic input normalization

    # Mock weather data for simplicity (matching Step 1 structure)
    mock_weather_db = mock_weather_db

    # Best Practice: Handle potential errors gracefully within the tool
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}
    


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() not in mock_weather_db.keys():
         return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }
    else:
        tz_identifier = "Asia/Shanghai"
   

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
        name="weather_time_agent", 
        model="gemini-2.0-flash-exp",
        description="""You are the main Weather and Time Agent, coordinating a team.
          - Your main task: Provide weather using the `get_weather` tool. and Provide time using `get_current_time`.
          - Delegation Rules: - If the user gives a simple greeting (like 'Hi', 'Hello'), delegate to `greeting_agent`. 
          - If the user gives a simple farewell (like 'Bye', 'See you'), delegate to `farewell_agent`. 
          - Handle weather requests yourself using `get_weather`. 
          - Handle time requests yourself using `get_current_time`. 
          - For other queries, state clearly if you cannot handle them.
          - I can look up chinese city name and translate it into english name automatically.
          """,
        tools=[get_weather, get_current_time], 
        sub_agents=[greeting_agent, farewell_agent]
)