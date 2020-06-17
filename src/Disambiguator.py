import CosineSimilarity


# -- count those elements that contain in token
def score_based_on_synsets(elements, tokens):
    score = 0.0
    for element in elements:
        if element in tokens:
            score += 1
    return score


def cosine_simm(tokens, example, def_string):
    vector = []
    # -- create an array from example and def_string words
    for i in example.split(" "):
        vector.append(i)
    for i in def_string.split(" "):
        vector.append(i)
    occurrences1 = {}
    occurrences2 = {}
    # -- count token's word repeat in master sentence(token)
    for word in tokens:
        old_count = occurrences1.get(word)
        if old_count is None:
            old_count = 0
        occurrences1[word] = old_count + 1
    # -- count vector's word repeat in master sentence(token)
    for word in vector:
        old_count = occurrences1.get(word)
        if old_count is None:
            old_count = 0
        occurrences2[word] = old_count + 1
    # -- Calculates the cosine similarity for two given vectors
    return CosineSimilarity.cosine_similarity(occurrences1, occurrences2)


def check_pos(synsets, input_pos, pos, ids, glosses, sem_cat, examples):
    for i in range(0, len(input_pos)):
        counter = len(synsets[i])
        target_pos = input_pos[i]
        for j in range(len(synsets[i]) - 1, -1):
            if target_pos != pos[i].get(j):
                del synsets[i][j]
                del pos[i][j]
                del ids[i][j]
                del glosses[i][j]
                del examples[i][j]
                del sem_cat[i][j]
                counter -= 1


def check_count(threshold, count, synsets, pos, ids, glosses, sem_cat, examples):
    for i in range(0, len(synsets)):
        for j in range(len(synsets[i]), 0):
            if count[i][j] < threshold:
                del synsets[i][j]
                del pos[i][j]
                del ids[i][j]
                del glosses[i][j]
                del examples[i][j]
                del sem_cat[i][j]


def remove_id(ignored_ids, synsets, pos, ids, glosses, sem_cat, examples):
    for i in range(0, len(synsets)):
        for j in range(len(synsets[i]), 0):
            if ids[i][j] in ignored_ids:
                del synsets[i][j]
                del pos[i][j]
                del ids[i][j]
                del glosses[i][j]
                del examples[i][j]
                del sem_cat[i][j]
