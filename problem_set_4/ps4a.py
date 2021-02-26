# Problem Set 4A
# Name: David Paul Wanjala
# Collaborators: None
# Time Spent: 30 min

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) <= 1:
        # if the sequence is one character or less, there is only one way to order it and thus return a list of the
        # single character
        return [sequence]
    else:
        permutations = []
        for e in get_permutations(sequence[:-1]):
            # we find permutation of a smaller portion of our sequence, one without the last item in the sequence
            # for each permutation e in the a permutation of the smaller version of the problem
            for i in range(len(e) + 1):
                # we append append the letter that we left out in all different ways we can insert this last character
                # into each permutation e and then append it to permutations
                permutations.append(e[:i] + sequence[-1] + e[i:])
        # we utilize set to avoid returning dublicates and the cast into a list
        return list(set(permutations))


if __name__ == '__main__':
    # EXAMPLE
    # example_input = 'abc'
    # print('Input:', example_input)
    # print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    # print('Actual Output:', get_permutations(example_input))

    # Put three example test cases here (for your sanity, limit your inputs
    # to be three characters or fewer as you will have n! permutations for a
    # sequence of length n)

    # example test case 1
    print('Input:', 'xy')
    print('Expected Output:', ['yx', 'xy'])
    print('Actual Output:', get_permutations('xy'))

    # example test case 2
    print('Input:', 'abc')
    print('Expected Output:', ['cab', 'bca', 'cba', 'bac', 'abc', 'acb'])
    print('Actual Output:', get_permutations('abc'))

    # example test case 3
    print('Input:', 'bob')
    print('Expected Output:', ['bbo', 'bob', 'obb'])
    print('Actual Output:', get_permutations('bob'))