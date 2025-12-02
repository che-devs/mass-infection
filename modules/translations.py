import json

class Translations():
    def __init__(self) -> None:

        files = [
            'de.json'
        ]

        self.translations = []
        for file in files:
            # Load translations an put them in list
            with open('lang/' + file, 'r', encoding='utf-8') as file:
                self.translations.append(json.load(file))

    def get_task(self, task: int, language: int = 0) -> str:
        match task:
            case 0:  # Clapping
                return self.translations[language]['task_1']
            case 1:  # Invite 3 Peoples
                return self.translations[language]['task_2']
            case 2:  # Invite 3 Peoples
                return self.translations[language]['task_3']
            case 3:  # Invite 3 Peoples
                return self.translations[language]['task_4']
            case 4:  # Invite 3 Peoples
                return self.translations[language]['task_5']
            case 5:  # Invite 3 Peoples
                return self.translations[language]['task_6']
            case 6:  # Invite 3 Peoples
                return self.translations[language]['task_7']
            case _:
                return '???'
    
    def get_nice(self, nice: int, language: int = 0) -> str:
        match nice:
            case 0:
                return self.translations[language]['nice_1']
            case 1:
                return self.translations[language]['nice_2']
            case 2:
                return self.translations[language]['nice_3']
            case 3:
                return self.translations[language]['nice_4']
            case 4:
                return self.translations[language]['nice_5']
            case 5:
                return self.translations[language]['nice_6']
            case _:
                return '???'
    
    def get_bad(self, bad: int, language: int = 0) -> str:
        match bad:
            case 0:
                return self.translations[language]['bad_1']
            case 1:
                return self.translations[language]['bad_2']
            case 2:
                return self.translations[language]['bad_3']
            case 3:
                return self.translations[language]['bad_4']
            case 4:
                return self.translations[language]['bad_5']
            case 5:
                return self.translations[language]['bad_6']
            case _:
                return '???'
    
    def get_general(self, general: int, language: int = 0) -> str:
        match general:
            case 0:
                return self.translations[language]['general_1']
            case 1:
                return self.translations[language]['general_2']
            case 2:
                return self.translations[language]['general_3']
            case 3:
                return self.translations[language]['general_4']
            case 4:
                return self.translations[language]['general_5']
            case 5:
                return self.translations[language]['general_6']
            case 6:
                return self.translations[language]['general_7']
            case _:
                return '???'


if __name__ == '__main__':
    from random import randint

    translation = Translations()
    print(translation.get_task(0))
    print(translation.get_nice(randint(0, 5)))
    print(translation.get_bad(0))
    print(translation.get_general(2))