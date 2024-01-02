import os
import sklearn
from joblib import load
from utils.read_files import find_latest_file_with_prefix_and_suffix
from ts2vec import TS2Vec
def load_svc(svc_folder:str, prefix="svc", suffix=".joblib"):
    """
    Loads latest svc from given folder
    """
    svc_path = find_latest_file_with_prefix_and_suffix(svc_folder, prefix, suffix)
    svc = load(os.path.join( svc_folder, svc_path))
    return svc

def load_net(net_folder:str, prefix="3_sensor_real_time_", suffix=".pth"):
    net_path = find_latest_file_with_prefix_and_suffix(net_folder, prefix, suffix)
    net = TS2Vec(input_dims=9, output_dims=9)
    return net.load(os.path.join(net_folder, net_path))

def load_label_encoder(label_folder:str, prefix="label_encoder", suffix=".joblib"):
    label_path = find_latest_file_with_prefix_and_suffix(label_folder, prefix, suffix)
    label_encoder = load(os.path.join(label_folder, label_path))
    return label_encoder

def classify(net, svc, window, label_encoder=None):
    embedding = net.encode(window, encoding_window="full_series")
    ans = svc.predict(embedding)
    if label_encoder is not None:
        ans = label_encoder.inverse_transform(ans)
    return ans

