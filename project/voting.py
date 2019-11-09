import random

def generate_random_survey(sug_list_songs):
    num_choices = len(sug_list_songs)
    num_shown = 2

    choice_list = randomize_choices(num_choices, num_shown)

    ret = []
    for i in choice_list:
        ret.append(sug_list_songs[i])
    return ret

def randomize_choices(num_choices, num_shown):
    poss_choices = []
    for i in range(0, num_shown + 1):
        poss_choices.append(set([]))

    for i in range(0, num_choices):
        choice = ChoiceRepr(i)
        poss_choices[0].add(choice)

    choice_list = []
    current_layer = 0

    while current_layer < num_shown:
        if len(poss_choices[current_layer]) <= 4:
            random_choice = random.sample(poss_choices[current_layer + 1], 4 - len(poss_choices[current_layer]))
            for choice in poss_choices[current_layer]:
                random_choice.append(choice)
            
            for choice in random_choice:
                choice_list.append(choice.id)
                poss_choices[choice.times_used].remove(choice)
                choice.times_used += 1
                if (choice.times_used <= num_shown):
                    poss_choices[choice.times_used].add(choice)

            current_layer += 1
        else:
            random_choice = random.sample(poss_choices[current_layer], 4)
            for choice in random_choice:
                choice_list.append(choice.id)
                poss_choices[choice.times_used].remove(choice)
                choice.times_used += 1
                poss_choices[choice.times_used].add(choice)
    
    return choice_list

class ChoiceRepr():
    id = 0
    times_used = 0

    def __init__(self, id):
        self.id = id
        self.times_used = 0
