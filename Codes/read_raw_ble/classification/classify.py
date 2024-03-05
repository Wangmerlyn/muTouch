import os
import math
from collections import Counter, deque
import sklearn
import numpy as np
from joblib import load
from utils.read_files import find_latest_file_with_prefix_and_suffix
from ts2vec import TS2Vec


def load_svc(svc_folder: str, prefix="svc", suffix=".joblib"):
    """
    Loads latest svc from given folder
    """
    svc_path = find_latest_file_with_prefix_and_suffix(
        svc_folder, prefix, suffix
    )
    svc = load(os.path.join(svc_folder, svc_path))
    return svc


def load_net(net_folder: str, prefix="3_sensor_real_time_", suffix=".pth"):
    net_path = find_latest_file_with_prefix_and_suffix(
        net_folder, prefix, suffix
    )
    net = TS2Vec(input_dims=9, output_dims=9, device="cpu")
    print(net_path)
    net.load(os.path.join(net_folder, net_path))
    return net


def load_label_encoder(
    label_folder: str, prefix="label_encoder", suffix=".joblib"
):
    label_path = find_latest_file_with_prefix_and_suffix(
        label_folder, prefix, suffix
    )
    # print(label_path)
    label_encoder = load(os.path.join(label_folder, label_path))
    return label_encoder


def classify(net, svc, window, label_encoder=None):
    embedding = net.encode(
        window.reshape(-1, 9)[np.newaxis, :, :], encoding_window="full_series"
    )
    ans = svc.predict(embedding)
    if label_encoder is not None:
        ans = label_encoder.inverse_transform(ans)
    return ans


def classify_3_stack(net, svc, window, label_encoder=None):
    sm_kernel = math.ceil(window.shape[0] / 3)
    embedding = net.encode(window.reshape(-1, 9)[np.newaxis,:,:]).squeeze()
    start_emb = np.max(embedding[:sm_kernel], axis=0)
    mid_emb = np.max(embedding[sm_kernel : 2 * sm_kernel], axis=0)
    end_emb = np.max(embedding[2 * sm_kernel :], axis=0)
    embedding = np.concatenate([start_emb, mid_emb, end_emb])
    ans = svc.predict(embedding[np.newaxis, :])
    if label_encoder is not None:
        ans = label_encoder.inverse_transform(ans)
    return ans


# count over queue
def queue_count(queue):
    counter = Counter(queue)
    return dict(counter)


def majority_vote(queue):
    counter = Counter(queue)
    return counter.most_common(1)[0][0]
