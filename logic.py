from const import *


def validate_word(string, valid_words):
    # this actually tests whether the string from input.echo_string is a valid
    # word, since the former just sanitizes for random bullshit like numbers
    if len(string) != len(wordle):
        return False
    elif string not in valid_words:
        return False
    else:
        return True


def compare_word(string, wordle, kb_dic):
    # this loop compares the chars in 'string' and 'wordle' based on index,
    # and assigns a color to the respective index in the color array. so
    # if string were 'weiss', and wordle were 'white', this function would
    # return something like this: ['weiss', [1,2,1,3,3]].
    # the structure for this is [string literal, [list of ints
    # referencing an assigned color]]. since the same letter can appear
    # multiple times in a word, we prefer to use the index i as a key
    # instead of a real dictionary, where repeated letters would all
    # point to the same color regardless of location.
    word_dic = string, [0 for c in string] # actually a list >_>
    for i in range(len(word_dic[0])):
            char = word_dic[0][i]
            if char == wordle[i]:
                color = green
            elif char in wordle:
                color = yellow
            else:
                color = grey
            word_dic[1][i] = color
            # this ensures 'better' colors have priority, i.e.
            # a previously green letter can't become yellow
            if kb_dic[char] < color:
                kb_dic[char] = color
    return word_dic
