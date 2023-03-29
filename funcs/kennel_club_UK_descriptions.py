''' call get_description() with the path to the kennel club csv and a dog_name
to get dog description data from kennel club'''

import pandas as pd
def clean_description_data(description_data):
    ''' convert the kennel_club_uk spreadsheet to a nicer format'''
    description_data['class'] = description_data['class'].map(str.capitalize)
    description_data['size_of_garden'] = description_data['size_of_garden'].map(lambda x: x.replace('/ medium', ''))
    description_data['home'] = description_data[['size_of_home', 'size_of_garden']].agg('<br>'.join, axis=1)
    description_data['town_or_country'] = description_data['town_or_country'].map({'Either': 'Yes', 'Country': 'No'})
    description_data['exercise'] = description_data['exercise'].map(lambda x: x.replace('per day', '').replace('Up to', '~').replace('More than', '>').replace('minutes', 'mins'))
    description_data['grooming'] = description_data['grooming'].map(lambda x: x.replace('More than', 'More than <br>'))
    description_data['lifespan'] = description_data['lifespan'].map(lambda x: x.replace('Over', '>').replace('Under', '<'))
    description_data['coat_length'] = description_data['coat_length'].map(lambda x: x.replace('&', '<br> &'))

    description_data.drop(columns = ['Position', 'vulnerable_native_breed', 'size_of_garden', 'size_of_home'], inplace = True)

    description_data.index.name = None
    description_data.columns = ['Class', 'Size', 'Daily exercise', 'Grooming', 'Fur length', 'Fur loss', 'Lifespan', 'City', 'Spacial needs']
    return description_data[['Class', 'Size', 'Lifespan', 'Daily exercise', 'Spacial needs', 'City', 'Fur length', 'Fur loss', 'Grooming']]


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
    }
    for word, correction in correction_dict.items():
        name = name.replace(word, correction)
    return name


def find_exact_kennel_entries(description_data, name):
    ''' returns all kennel_club UK entries with indexes that contain ALL words of species_name (order doesn't matter)
    e.g. Standard Poodle is going to be recognized as Poodle (Standard)'''
    index_in_kennel_data = description_data.index.map(lambda kennel_entry: all(word in kennel_entry for word in name.split()))
    return description_data[index_in_kennel_data]


def find_approximate_kennel_entries(description_data, name):
    ''' # returns kennel_club UK entries with indexes that contains ONE word of species_name ; common words like "dog" or "hound" are ignored'''
    ignore_list = ['Dog', 'English', 'Terrier', 'American', 'Spaniel', 'Haired', 'Wire', 'Japanese', 'Hound', 'Scottish']
    for word in ignore_list:
        name = name.replace(word, '')
    index_in_kennel_data = description_data.index.map(lambda kennel_entry: any(word in kennel_entry for word in name.split()))
    return description_data[index_in_kennel_data]


def remove_exceptions(descriptions, name):
    ''' hard coding for unwanted matches that were not removed automatically;
    if the dog name matches a key of exceptions, the corresponding row of
    from description is dropped '''
    exceptions_dict = {'Collie': 'Border Collie'}
    if name in exceptions_dict.keys():
        corrected_descriptions = descriptions.drop(exceptions_dict[name], axis=0)
        return corrected_descriptions
    return descriptions


def get_description(description_data_path, species_name:str):
    ''' takes the name of a dog breed and looks for corresponding entries in the kennel club UK data
    returns a DataFrame with all matching entries
    First, checks for exact matches
    If no exact matches are found, looks for matches that contain all words of species_name
    If there are still no matches, looks for entries that contain any word of species_name
    '''
    description_data = pd.read_csv(description_data_path, index_col='breed_name')
    description_data = clean_description_data(description_data)
    cleaned_name = clean_name(species_name)
    if cleaned_name in description_data.index:
        descriptions = description_data.loc[[cleaned_name],:]
    elif not find_exact_kennel_entries(description_data, cleaned_name).empty:
        descriptions = find_exact_kennel_entries(description_data, cleaned_name)
    else:
        descriptions = find_approximate_kennel_entries(description_data, cleaned_name)
    return remove_exceptions(descriptions, cleaned_name).style
    # .style is necessary so that the output shows the "<br>" introduced in
    #  clean_description_data as linebreaks in the dataframe
