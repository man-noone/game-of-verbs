import os
import json

import dialogflow_v2


GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
DIALOGFLOW_PROJECT_ID = os.environ['DIALOGFLOW_PROJECT_ID']


class IntentWrapper:
    def __init__(self, name, questions, answers):
        self._name = name

        self._questions = questions
        if not isinstance(questions, list):
            self._questions = [questions]

        self._answers = answers
        if not isinstance(answers, list):
            self._answers = [answers]

        self._training_phrases = self._create_training_phrases(self._questions)
        self._messages = self._create_messages(self._answers)

        self.intent = self._create_intent(self._name, self._training_phrases, self._messages)


    def _create_training_phrases(self, questions):
        parts = [dialogflow_v2.types.Intent.TrainingPhrase.Part(text=question) \
                 for question in questions]
        return [dialogflow_v2.types.Intent.TrainingPhrase(type=0, parts=[part]) \
                for part in parts]

    def _create_messages(self, answers):
        texts = [dialogflow_v2.types.Intent.Message.Text(text=[answer]) \
                 for answer in answers]
        return [dialogflow_v2.types.Intent.Message(text=text) for text in texts]

    def _create_intent(self, display_name, training_phrases, messages=[]):
        return dialogflow_v2.types.Intent(display_name=display_name,
                                          training_phrases=training_phrases,
                                          messages=messages)


def main():
    with open('questions.json') as file:
        training_phrases = json.load(file)

    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(DIALOGFLOW_PROJECT_ID)

    for category in training_phrases:
        questions = training_phrases[category]['questions']
        answer = training_phrases[category]['answer']

        iw = IntentWrapper(category, questions, answer)
        response = client.create_intent(parent, iw.intent)



if __name__ == '__main__':
    main()
