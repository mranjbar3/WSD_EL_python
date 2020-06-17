import math

"""
 * Calculates the cosine similarity for two given vectors.
 *
 * @param leftVector left vector
 * @param rightVector right vector
 * @return cosine similarity between the two vectors
"""


def cosine_similarity(left_vector, right_vector):
    if left_vector is None or right_vector is None:
        raise Exception("Vectors must not be null")

    intersection = get_intersection(left_vector, right_vector)

    dot_product = dot(left_vector, right_vector, intersection)
    d1 = 0.0
    for value in left_vector.values():
        d1 += value ** 2
    d2 = 0.0
    for value in right_vector.values():
        d2 += value ** 2
    cosine_similarity_var = 0.0
    if d1 > 0.0 and d2 > 0.0:
        cosine_similarity_var = dot_product / (math.sqrt(d1) * math.sqrt(d2))
    return cosine_similarity_var


"""
 * Returns a set with strings common to the two given maps.
 *
 * @param leftVector left vector map
 * @param rightVector right vector map
 * @return common strings
 """


def get_intersection(left_vector, right_vector):
    intersection = []
    for vector in left_vector:
        if right_vector.get(vector) is not None:
            intersection.append(vector)
    return intersection


"""
 * Computes the dot product of two vectors. It ignores remaining elements. It means
 * that if a vector is longer than other, then a smaller part of it will be used to compute
 * the dot product.
 *
 * @param leftVector left vector
 * @param rightVector right vector
 * @param intersection common elements
 * @return the dot product
"""


def dot(left_vector, right_vector, intersection):
    dot_product = 0
    for key in intersection:
        dot_product += left_vector.get(key) * right_vector.get(key)
    return dot_product
