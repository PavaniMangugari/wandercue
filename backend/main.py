from agents.coordinator_agent import run_wandercue

destination = input("Enter destination: ")
available_time = input("Enter available time: ")
interests_text = input("Enter interests separated by commas: ")

interests = [item.strip() for item in interests_text.split(",")]

result = run_wandercue(
    destination,
    available_time,
    interests
)

print(result)
