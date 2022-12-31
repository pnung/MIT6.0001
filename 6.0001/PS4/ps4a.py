import random


def get_permutations(sequence):
    permutation = ""
    permutations = []
    sequence_list = list(sequence)
    if sequence == permutation:
        return permutations
    else:
        for j in range(len(sequence)):
            print(sequence_list)
            permutations.append(str(sequence_list))
            sequence_list[j], sequence_list[j+1] = sequence_list[j+1], sequence_list[j]
            if str(sequence_list) in permutations:
                continue
            else:
                permutations.append(str(sequence_list))
            print(permutations)



if __name__ == '__main__':
   example_input = 'abc'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))
