import numpy as np
import cython
cimport numpy as np


@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def skipgrams(
    sequence,
    int vocabulary_size,
    np.ndarray[np.float_t, ndim=1] sampling_table,
    int window_size=4,
    int negative_samples=1,
    bint shuffle=1,
    bint categorical=0,
    int seed=0
    ):
    """Generates skipgram word pairs.
    This function transforms a sequence of word indexes (list of integers)
    into tuples of words of the form:
    - (word, word in the same window), with label 1 (positive samples).
    - (word, random word from the vocabulary), with label 0 (negative samples).
    Read more about Skipgram in this gnomic paper by Mikolov et al.:
    [Efficient Estimation of Word Representations in
    Vector Space](http://arxiv.org/pdf/1301.3781v3.pdf)
    # Arguments
        sequence: A word sequence (sentence), encoded as a list
            of word indices (integers). If using a `sampling_table`,
            word indices are expected to match the rank
            of the words in a reference dataset (e.g. 10 would encode
            the 10-th most frequently occurring token).
            Note that index 0 is expected to be a non-word and will be skipped.
        vocabulary_size: Int, maximum possible word index + 1
        window_size: Int, size of sampling windows (technically half-window).
            The window of a word `w_i` will be
            `[i - window_size, i + window_size+1]`.
        negative_samples: Float >= 0. 0 for no negative (i.e. random) samples.
            1 for same number as positive samples.
        shuffle: Whether to shuffle the word couples before returning them.
        categorical: bool. if False, labels will be
            integers (eg. `[0, 1, 1 .. ]`),
            if `True`, labels will be categorical, e.g.
            `[[1,0],[0,1],[0,1] .. ]`.
        sampling_table: 1D array of size `vocabulary_size` where the entry i
            encodes the probability to sample a word of rank i.
        seed: Random seed.
    # Returns
        couples, labels: where `couples` are int pairs and
            `labels` are either 0 or 1.
    # Note
        By convention, index 0 in the vocabulary is
        a non-word and will be skipped.
    """
    cdef np.ndarray[np.int_t,
                    negative_indices=False,
                    mode='c'] v_sequence = np.array(sequence)

    cdef int i, seqlen, wi, window_start, window_end, num_negative_samples

    seqlen = v_sequence.shape[0]

    cdef np.ndarray[np.float_t,
                    negative_indices=False,
                    mode='c'] sampling_table_rand = np.random.random(seqlen)

    cdef np.ndarray[np.int_t,
                    negative_indices=False,
                    mode='c'] negative_index_array

    cdef np.ndarray[np.int_t, ndim=2,
                    negative_indices=False,
                    mode='c'] couples_arr

    cdef np.ndarray[np.int_t,
                    negative_indices=False,
                    mode='c'] labels_arr

    cdef np.ndarray[np.int_t,
                    negative_indices=False] words_arr

    cdef np.ndarray[np.int_t,
                    negative_indices=False,
                    mode='c'] shuffle_idx

    cdef int data_idx = 0
    # Define maximum possible return size
    # seqlen * (window_size * 2) * (1 + negative_samples)
    cdef int max_data_size = seqlen * (window_size * 2) * (1 + negative_samples)
    couples_arr = np.zeros((max_data_size, 2), dtype=np.int)
    labels_arr = np.ones(max_data_size, dtype=np.int)


    for i in range(seqlen):
        wi = v_sequence[i]
        if not wi:
            continue
        # if sampling_table is not None:
        r = sampling_table_rand[i]
        if sampling_table[wi] < r:
            continue

        window_start = max(0, i - window_size)
        window_end = min(seqlen, i + window_size + 1)
        for j in range(window_start, window_end):
            if j != i:
                wj = v_sequence[j]
                if not wj:
                    continue

                couples_arr[data_idx][0] = wi
                couples_arr[data_idx][1] = wj
                labels_arr[data_idx] = 1
                data_idx += 1

    if negative_samples > 0:
        num_negative_samples = data_idx * negative_samples

        # Note that np.random.randint is exclusive of `high` while random.randint is inclusive of `high`
        # This means that if random.random is used, subtract a 1 to the `vocabulary_size`.
        negative_index_array = np.random.randint(1, vocabulary_size, num_negative_samples)

        words_arr = couples_arr[:data_idx, 0]
        np.random.shuffle(words_arr)

        words_arr = np.tile(words_arr, negative_samples)

        couples_arr[data_idx:data_idx+num_negative_samples, 0] = words_arr
        couples_arr[data_idx:data_idx+num_negative_samples, 1] = negative_index_array
        labels_arr[data_idx:data_idx+num_negative_samples] = 0

        data_idx += num_negative_samples

    couples_arr = couples_arr[:data_idx]
    labels_arr = labels_arr[:data_idx]

    if shuffle:
        if seed == 0:
            seed = np.random.randint(0, 10e6)

        np.random.seed(seed)
        shuffle_idx = np.random.choice(range(data_idx), data_idx, replace=False)

        couples_arr = couples_arr[shuffle_idx]
        labels_arr = labels_arr[shuffle_idx]

    return couples_arr, labels_arr
