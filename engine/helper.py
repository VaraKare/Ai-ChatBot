import re


def extract_yt_term(command):
    #define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    #use research to find the match in the command
    match = re.search(pattern,command,re.IGNORECASE)
    if match:
        return match.group(1)  # Return the captured group (search term)
    else:
        return None  # Return None if no match is found

def remove_words(input_string, words_to_remove):
    #split the input string into words 
    words = input_string.split()

    #remove unwanted words
    filter_words = [word for word in words if word.lower() not in words_to_remove ]
    #join the remaining words back into a string
    result_string =' '.join(filter_words)
    return result_string