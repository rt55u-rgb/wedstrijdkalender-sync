from parser import load_matches
from calendar_sync import GoogleCalendar

print("Wedstrijden laden...")
matches = load_matches()

print(f"{len(matches)} wedstrijden gevonden")

calendar = GoogleCalendar()

print("Agenda ophalen...")
event_index = calendar.build_index()

excel_ids = set()

added = 0
updated = 0
deleted = 0

print("\nSynchroniseren...\n")

for match in matches:

    excel_ids.add(match.uid)

    if match.uid in event_index:

        calendar.update_match(
            event_index[match.uid],
            match
        )

        updated += 1

    else:

        calendar.add_match(match)

        added += 1


for uid, event in event_index.items():

    if uid not in excel_ids:

        calendar.delete_event(event)

        deleted += 1


print("\n--------------------------------")

print(f"Toegevoegd : {added}")
print(f"Bijgewerkt : {updated}")
print(f"Verwijderd : {deleted}")

print("--------------------------------")
print("Synchronisatie voltooid.")