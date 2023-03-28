''' call get_description() with the path to the kennel club csv and a dog_name
to get dog description data from kennel club'''

import pandas as pd


def clean_name(name):
    ''' converts dog name to match the names used by the kennel club UK'''
    name = name.replace('-and-', ' & ')
    name = name.replace('_', ' ')
    name = name.replace('-', ' ')
    name = ' '.join(map(str.capitalize,name.split(' ')))

    correction_dict = {
        'Greater': 'Great',
        'Short Haired': 'Shorthaired',
        'Long Haired': 'Longhaired',
        'Bullterrier': 'Bull Terrier',
        'Scotch': 'Scottish',
        'Saint': 'St.',
        'Bull Mastiff': 'Bullmastiff',
        'Great Pyrenees': 'Pyrenean Mountain Dog',
        'Standard Schnauzer': 'Schnauzer',
        'Japanese Spaniel': 'Japanese Chin',
        'Boston Bull': 'Boston Terrier',
        'Brabancon Griffon': 'Griffon Bruxellois',
        'Haired': '',
        'Mexican': 'Mex',
        'Pekinese': 'Pekingese',
        'Basset': 'Basset Hound',
        'Bull Dog': 'Bulldog',
        'Schnauzer Standard': 'Schnauzer',
        'Blenheim Spaniel': 'King Charles Spaniel'
        'Bluetick'
    }
    for word, correction in correction_dict.items():
        name = name.replace(word, correction)
    return name


def find_exact_kennel_entries(name, description_data):
    ''' returns all kennel_club UK entries with indexes that contain ALL words of species_name (order doesn't matter)
    e.g. Standard Poodle is going to be recognized as Poodle (Standard)'''

    index_in_kennel_data = description_data.index.map(lambda kennel_entry: all(word in kennel_entry for word in name.split()))
    return description_data[index_in_kennel_data]


def find_approximate_kennel_entries(name, description_data):
    ''' # returns kennel_club UK entries with indexes that contains ONE word of species_name ; common words like "dog" or "hound" are ignored'''

    ignore_list = ['Dog', 'English', 'Terrier', 'American', 'Spaniel', 'Haired', 'Wire', 'Japanese', 'Hound', 'Scottish']
    for word in ignore_list:
        name = name.replace(word, '')
    index_in_kennel_data = description_data.index.map(lambda kennel_entry: any(word in kennel_entry for word in name.split()))
    return description_data[index_in_kennel_data]


def get_description(description_data_path, species_name:str):
    ''' takes the name of a dog breed and looks for corresponding entries in the kennel club UK data
    returns a DataFrame with all matching entries
    First, checks for exact matches
    If no exact matches are found, looks for matches that contain all words of species_name
    If there are still no matches, looks for entries that contain any word of species_name
    '''
    description_data = pd.read_csv(description_data_path, index_col='breed_name')
    cleaned_name = clean_name(species_name)
    #print(f'Showing results for {correction} instead of {word}')
    if cleaned_name in description_data.index:
        return description_data.loc[[cleaned_name],:]
    if not find_exact_kennel_entries(cleaned_name, description_data).empty:
        return find_exact_kennel_entries(cleaned_name, description_data)
    return find_approximate_kennel_entries(cleaned_name, description_data)
