import json
import re


def intent_samples_to_comment(samples):
    """
    Takes a list of intent sample utterance and returns a python comment for an alexa intent python constant
    """
    # Wrap all the sample strings in quote marks
    samples = list(map(lambda sample: "'" + sample + "'", samples))

    return '# Samples phrases : ' + ', '.join(samples)


def intent_name_to_constant(intent_name):
    """
    Takes a string containing the name of a alexa intent and returns the a python constant declaration for that intent
    """
    intent_name_declaration = intent_name

    intent_name_declaration = intent_name_declaration.replace('Intent', '').replace('AMAZON.', '')

    intent_name_declaration = re.sub(r"(?<![A-Z])(?<!^)([A-Z])", r"_\1", intent_name_declaration)

    intent_name_declaration = intent_name_declaration.upper()

    return intent_name_declaration + " = '" + intent_name + "'"


def generate_alexa_intents_from_alexa_json():
    python_out_file = open('output/alexa_intents.py', 'w+')

    with open('input/alexa_interaction.json') as json_in_file:
        data = json.load(json_in_file)

        python_out_file.writelines('class Intents:\n')

        for intent in data['interactionModel']['languageModel']['intents']:
            python_out_file.write('\n    ' + intent_samples_to_comment(intent['samples']) + '\n')

            python_out_file.write('    ' + intent_name_to_constant(intent['name']) + '\n')
