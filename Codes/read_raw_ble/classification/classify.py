import math
import os
from collections import Counter

import numpy as np
from joblib import load
from ts2vec import TS2Vec

from utils.read_files import find_latest_file_with_prefix_and_suffix


def load_svc(svc_folder: str, prefix="svc", suffix=".joblib"):
    """Load the latest SVC from the given folder."""
    svc_path = find_latest_file_with_prefix_and_suffix(svc_folder, prefix, suffix)
    return load(os.path.join(svc_folder, svc_path))


def load_net(net_folder: str, prefix="3_sensor_real_time_", suffix=".pth"):
    """Load the latest TS2Vec checkpoint."""
    net_path = find_latest_file_with_prefix_and_suffix(net_folder, prefix, suffix)
    net = TS2Vec(input_dims=9, output_dims=9, device="cpu")
    net.load(os.path.join(net_folder, net_path))
    return net


def load_label_encoder(label_folder: str, prefix="label_encoder", suffix=".joblib"):
    """Load the latest label encoder."""
    label_path = find_latest_file_with_prefix_and_suffix(label_folder, prefix, suffix)
    return load(os.path.join(label_folder, label_path))


def classify(net, svc, window, label_encoder=None):
    """Classify a window with TS2Vec + SVC pipeline."""
    embedding = net.encode(
        window.reshape(-1, 9)[np.newaxis, :, :], encoding_window="full_series"
    )
    ans = svc.predict(embedding)
    if label_encoder is not None:
        ans = label_encoder.inverse_transform(ans)
    return ans


def classify_3_stack(net, svc, window, label_encoder=None, sm_kernel=10):
    """Classify using 3-stack pooling."""
    _segment_length = math.ceil(window.shape[0] / 3)
    embedding = net.encode(window.reshape(-1, 9)[np.newaxis, :, :]).squeeze()
    start_emb = np.max(embedding[:sm_kernel], axis=0)
    mid_emb = np.max(embedding[sm_kernel : 2 * sm_kernel], axis=0)
    end_emb = np.max(embedding[2 * sm_kernel :], axis=0)
    embedding = np.concatenate([start_emb, mid_emb, end_emb])
    ans = svc.predict(embedding[np.newaxis, :])
    if label_encoder is not None:
        ans = label_encoder.inverse_transform(ans)
    return ans


def queue_count(queue) -> dict:
    """Count the occurrences of each item in a queue."""
    counter = Counter(queue)
    return dict(counter)


def majority_vote(queue):
    """Determine the most common element in a queue."""
    if not queue:
        return None
    counter = Counter(queue)
    return counter.most_common(1)[0][0]
