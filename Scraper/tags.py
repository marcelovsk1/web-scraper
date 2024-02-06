import openai
import json
from apikey

def generate_tags(event_titles):
    tags = []
    openai.api_key = "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"

    for title in event_titles:
        prompt = f"Generate tags for the event title: {title}. Tags:"
        response = openai.Completion.create(
            model="text-curie-001",
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

# Exemplo de uso:
add_tags_to_events("events_data.json")

# import json
# import re

# def generate_tags(event_titles):
#     tags = []
#     for title in event_titles:
#         if title is not None:  # Verificar se o título não é nulo antes de processá-lo
#             # Aplicar regras simples para extrair tags dos títulos dos eventos
#             if "concert" in title.lower():
#                 tags.append("#Music #Live")
#             elif "market" in title.lower():
#                 tags.append("#Market #Shopping")
#             elif "festival" in title.lower():
#                 tags.append("#Festival #Music #Food")
#             else:
#                 tags.append("#Other")
#         else:
#             tags.append("#Other")  # Se o título for nulo, adicione uma tag padrão

#     return tags

# def add_tags_to_events(events_data_file):
#     with open(events_data_file, 'r') as file:
#         data = json.load(file)

#     for source_data in data:
#         events = source_data.get('events', [])  # Obter a lista de eventos ou uma lista vazia se não existir
#         event_titles = [event['Event'] for event in events if 'Event' in event]  # Obter os títulos dos eventos apenas se existirem

#         if event_titles:  # Verificar se event_titles não está vazio antes de chamar generate_tags
#             tags = generate_tags(event_titles)

#             for event, tag in zip(events, tags):
#                 event['Tags'] = tag

#     with open(events_data_file, 'w') as file:
#         json.dump(data, file, indent=2)

# # Exemplo de uso:
# add_tags_to_events("events_data.json")
