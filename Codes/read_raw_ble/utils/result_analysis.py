from collections import Counter, deque


# count over queue
def queue_count(queue):
    counter = Counter(queue)
    return dict(counter)


def majority_vote(queue):
    counter = Counter(queue)
    return counter.most_common(1)[0][0]


if __name__ == "__main__":
    print(
        majority_vote(deque(["apple", "banana", "apple", "orange", "banana", "apple"]))
    )
