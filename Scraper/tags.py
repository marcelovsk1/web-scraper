import openai
import json

def generate_tags(event_titles):
    tags = []
    openai.api_key = "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"

    for title in event_titles:
        prompt = f"Generate tags for the event title: {title}. Tags:"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=30,
            stop=["\n"]
        )
        generated_tags = response.choices[0].text.strip()
        tags.append(generated_tags)

    return tags

def add_tags_to_events(events_data_file):
    with open(events_data_file, 'r') as file:
        data = json.load(file)

    for source_data in data:
        events = source_data['events']
        event_titles = [event['Event'] for event in events]
        tags = generate_tags(event_titles)

        for event, tag in zip(events, tags):
            event['Tags'] = tag

    with open(events_data_file, 'w') as file:
        json.dump(data, file, indent=2)

add_tags_to_events("events_data.json")
