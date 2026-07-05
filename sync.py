from parser import load_matches
from calendar_sync import GoogleCalendar

matches = load_matches()

calendar = GoogleCalendar()

for match in matches:
    calendar.add_match(match)

print(f"\n{len(matches)} wedstrijden gesynchroniseerd.")
