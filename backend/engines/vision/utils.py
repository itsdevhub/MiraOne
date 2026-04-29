def landmark_distance(normalized_landmark_1, normalized_landmark_2):
    return ((normalized_landmark_1.x - normalized_landmark_2.x)**2 + (normalized_landmark_1.y - normalized_landmark_2.y)**2) ** 0.5
