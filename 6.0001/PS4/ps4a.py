def get_permutations(string):
    permutations = []
    if len(string) == 1:
        return [string]
    else:
        for char in string:
            [permutations.append(char + a) for a in get_permutations(string.replace(char, "", 1))]
    return permutations

if __name__ == '__main__':
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))