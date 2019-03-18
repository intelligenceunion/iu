import math
import random
import itertools

def partition(iterable, size):
    """
    Partition the given iterable into multiple chunks.

    Example:
    >>> list(partition(range(10), 3))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    # make sure we return generator, for performance reasons.
    >>> import types; isinstance(partition(range(10), 3), types.GeneratorType)
    True
    """
    return ([snd for fst, snd in grpiter] for (grpidx, grpiter) in itertools.groupby(enumerate(iterable), lambda (idx, elem) : idx / size))

def keydict(iterable, key):
    '''
    from a given iterable and a key function, create a dictionary where
    keys are generated by key function.

    >>> keydict(['hello','world'], key=lambda x: x[0])
    {'h': 'hello', 'w': 'world'}

    '''
    return dict((key(item), item) for item in iterable)

def uniquify(iterable, **kwargs):
    '''

    key(optional) - key function used to uniquify elements. default to the
      identity function.
    sort(optional) - key function used in sorting.
      defaults to the key function
    reverse(optional) - sorting order. default is false.'

    >>> uniquify(['apple','banana','apple','bananana','banana'])
    ['apple', 'banana', 'bananana']
    '''
    # expected kwargs:

    # key(optional) - key function used to uniquify elements. default to the
    #   identity function.
    # sort(optional) - key function used in sorting.
    #   defaults to the key function
    # reverse(optional) - sorting order. default is false.'

    key = kwargs.get('key', lambda x : x)
    sort = kwargs.get('sort', key)
    reverse = kwargs.get('reverse', False)
    if not (set(kwargs.keys()) <= set(['key','sort','reverse'])):
        raise TypeError, 'invalid arguments.'
    dictionary = keydict(iterable, key=key)
    return sorted(dictionary.itervalues(),
        key=lambda v: sort(v),
        reverse=reverse)

def ilen(iterator):
    '''
        Returns the length of an iterator.
        One quick way to do this is by
        len(list(iterator))
        but we have to allocate potentially large list.
    '''
    return sum(1 for _ in iterator)

def iterate_multiple_elements(iterator, num_elements):
    '''An iterator to return a certain number of elements at a time.

    Args:
        iterator -- Iterator to iterate over
        num_elements -- Number of elements to return in each iteration
    '''
    a = iter(iterator)
    for t in itertools.izip(*[a for _ in range(num_elements)]):
        yield t

    num_remaining_items = len(iterator) % num_elements
    if num_remaining_items:
        remaining_items = iterator[-num_remaining_items:]
        yield remaining_items

# from python itertools recipes
def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = itertools.cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = itertools.cycle(itertools.islice(nexts, pending))


# insert that preseves original order in f_list
# f_list: list of elements to be inserted into.
# m_list: list of elements to insert.
def ordered_insert(f_list, m_list, one_per_n):
    if m_list is None:
        m_list = []
    for i, elem in enumerate(m_list):
        pos = one_per_n * i + random.randint(0, one_per_n - 1)
        f_list.insert(pos, elem)
    return f_list

#
def weighted_sample(pairs, size):
    results = []
    for item, weight in pairs:
        weight_rand = math.log(random.random())/weight
        pair = [item, weight_rand]
        results.append(pair)

    sorted_sample =  sorted(results, reverse=True)[:size]
    return [r[0] for r in sorted_sample]

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)