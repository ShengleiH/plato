from folgen.fol_util import *
from nlgen_scripts.runfol import runfol
import random
import requests
from tqdm import tqdm

NUM_SENTENCES = 10

def generate_depth_k_sentences(k=1):
    # build the template formulas
    predicates = read_predicate_file('folgen/predicates.txt')
    constants = read_constant_file('folgen/constants.txt')
    preds = [
        "%s(%s)" % (pred, ','.join(['%s' for _ in range(arity)]))
        for pred, arity in predicates
    ]

    operators = read_operator_file('folgen/operators.txt')

    # memoize results
    memo = {}

    def recurse(depth):
        if depth == 0:
            return preds

        if depth in memo:
            return memo[depth]

        # generate all depth k trees
        if depth-1 not in memo:
            subtrees = recurse(depth-1)
            memo[depth-1] = tuple(subtrees)
        else:
            subtrees = memo[depth-1]

        ret = []
        for operator in operators:
            for i in range(len(subtrees)):
                for j in range(len(subtrees)):
                    if depth == k:
                        ret.append('%s%s%s' % (subtrees[i], operator, subtrees[j]))
                    else:
                        ret.append('(%s%s%s)' % (subtrees[i], operator, subtrees[j]))

        memo[depth] = ret
        return ret

    depth_k_trees = recurse(k)
    for tree in depth_k_trees[:5]:
        print tree

    count = 0
    for tree in depth_k_trees:
        count += (tree.count('%s') * NUM_SENTENCES)

    # get
    arg_train = [constants[i%len(constants)] for i in range(count)]
    random.shuffle(arg_train)

    with open('folgen/k%d_sents.out' % k, 'w') as w:
        for tree in tqdm(depth_k_trees):
            n = tree.count('%s')
            for i in range(NUM_SENTENCES):
                formula = tree % tuple(arg_train[:n])
                arg_train = arg_train[n+1:]
                sents = get_post_request(formula)
                for sent in set(sents):
                    if len(sent) == 0:
                        continue
                    w.write(sent+'\t'+formula+'\n')

def get_post_request(fol):
    url = 'http://cypriot.stanford.edu:8080/ace/'
    payload = {
        'sig':fol,
        'rulefile':'rules.all',
        'blockfile':'rules.none'
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.text.split('\n')
    else:
        return []

def generate_atomic_sentences():
    with open('folgen/atomic_sents.out', 'w') as w:
        with open('folgen/atoms.out', 'r') as f:
            for line in tqdm(f):
                atom = line.rstrip()
                sents = get_post_request(atom)
                for sent in sents:
                    if len(sent) == 0:
                        continue
                    w.write(sent+'\t'+atom+'\n')

if __name__ == '__main__':
    # predicates = read_predicate_file('folgen/predicates.txt')
    # constants = read_constant_file('folgen/constants.txt')
    # atoms = generate_all_atoms(predicates, constants)
    # with open('folgen/atoms.out', 'w') as w:
    #     for atom in atoms:
    #         w.write('%s\n' % atom)

    # generate_all_sentences()
    # generate_atomic_sentences()
    generate_depth_k_sentences(k=1)
    # print get_post_request('(tet(FORMAT)&tet(FORMAT))')