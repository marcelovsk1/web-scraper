import json

def filter_events(events_data, event_name, date, location, image_url):
    filtered_events = []
    seen_events = set()

    with open(events_data, 'r') as file:
        data = json.load(file)

    for source_data in data:
        source_name = source_data['source_name']
        events = source_data['events']

        for event in events:
            event_key = (event[event_name], event[date], event[location], event[image_url])
            if event_key not in seen_events:
                seen_events.add(event_key)
                filtered_events.append({
                    'source_name': source_name,
                    'event_name': event[event_name],
                    'date': event[date],
                    'location': event[location],
                    'image_url': event[image_url]
                })

    return filtered_events

filtered_events = filter_events("events_data.json", "Event", "Date", "Location", "Image URL")
# Convert to JSON
filtered_events_json = json.dumps(filtered_events, indent=2)
print(filtered_events_json)

# Plese run and test this code in your device before apply into the app
