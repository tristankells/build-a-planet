import json


def generate_slot_list_from_alexa_json():
    python_out_file = open('output/slot_type_list.py', 'w+')

    with open('input/alexa_interaction.json') as json_in_file:
        data = json.load(json_in_file)

        for types in data['interactionModel']['languageModel']['types']:
            python_out_file.write((types['name']) + ' = [')

            slot_values_string = ''

            for value in types['values']:
                slot_values_string += '"' + value['name']['value'].lower() + '",'

            python_out_file.write(slot_values_string[:-1])
            python_out_file.write(']\n')
