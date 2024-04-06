# Training day that rule changed
rule_change = {
    'JC240': 9,
    'JC241': 14,
    'JC258': 11,
    'JC267': 4,
    'JC274': 12,
    'JC283': 14,
    'JC315': 14, # needs to be edited
}

cscheme = {
    'JC240': 'gray',
    'JC241': 'gray',
    # 'JC258' : '#EF767A',
    # 'JC267' : '#1D2F6F',
    # 'JC274' : '#49BEAA',
    # 'JC283' : '#1A8FE3',
    'JC258' : '#1b9e77',
    'JC267' : '#66a61e',
    'JC274' : '#7570b3',
    'JC283' : '#d95f02',
    'JC315' : '#e7298a',
    'JC258_light' : '#e0f3ed',
    'JC267_light' : '#fae8f3',
    'JC274_light' : '#fee8e0',
    'JC283_light' : '#dde3ef',
    'JC315_light' : '#fef0f7',
    'JC258_medium' : '#d1ede4',
    'JC267_medium' : '#f8dced',
    'JC274_medium' : '#feddd0',
    'JC283_medium' : '#d1d9ea',
    'JC315_medium' : '#fdeaf3',
    'C' : "#593510",
    'H' : "#fcbe15",
    'S' : "#d2c28f",
    'other' : "maroon",
    }

cue_names = {
    'chocolate' : "#593510",
    'cereal' : "#fcbe15",
    'sunflower' : "#d2c28f",
}

# reward arms: C. H, S
reward_arms = {
    'JC240': [3, 7, 1],
    'JC241': [3, 7, 1],
    'JC258': [3, 7, 1],
    'JC267': [3, 7],
    'JC274': [8, 4, 5],
    'JC283': [8, 3, 5],
    'JC315': [3, 4, 7],
}