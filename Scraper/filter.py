import json

def filter_events(events_data, event_name, date, location, image_url):
    # Lista para armazenar os eventos filtrados
    # Conjunto para rastrear os eventos únicos que já foram vistos
    filtered_events = []
    seen_events = set()

    # Open the JSON File
    with open(events_data, 'r') as file:
        data = json.load(file)

    # Itera sobre os dados carregados do arquivo JSON
    for source_data in data:
        # Obtém o nome da fonte dos eventos
        source_name = source_data['source_name']
        # Obtém a lista de eventos da fonte atual
        events = source_data['events']

        # Itera sobre os eventos da fonte atual
        for event in events:
            # Cria uma chave composta pelos valores do evento que servirá como identificador único
            event_key = (event[event_name], event[date], event[location], event[image_url])
            # Verifica se o evento já foi visto antes
            if event_key not in seen_events:
                # Se o evento for único, adiciona sua chave ao conjunto de eventos vistos
                seen_events.add(event_key)
                # Adiciona o evento à lista de eventos filtrados
                filtered_events.append({
                    'source_name': source_name,
                    'event_name': event[event_name],
                    'date': event[date],
                    'location': event[location],
                    'image_url': event[image_url]
                })

    return filtered_events

# Chama a função filter_events e passa o nome do arquivo de dados de eventos e os nomes das chaves relevantes
filtered_events = filter_events("events_data.json", "Event", "Date", "Location", "Image URL")

# Convert to JSON
filtered_events_json = json.dumps(filtered_events, indent=2)
print(filtered_events_json)
