from multiprocessing import Pool
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from parse import parse

# New method


def data_mapping(data):
    readingi = np.fromstring(data[1:-1], dtype=float, sep=", ")
    return readingi


def time_mapping(t):
    tdata = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
    origin_day = datetime(year=tdata.year, month=tdata.month, day=tdata.day)
    tstamp = (tdata - origin_day).total_seconds()
    return tstamp


def read_data(file_path):
    data = []
    with open(file_path, "rb") as f:
        i = -1
        flag = False
        nsensor = 0
        for line in f.readlines():
            i += 1
            if i == 0:
                continue
            line_decoded = line.decode("utf-8")
            if line_decoded.startswith("#"):
                if not flag and i > 1:
                    nsensor = i - 3
                    flag = True
                continue
            elif "Hz" in line_decoded:
                continue
            tmp = line_decoded.split(":")[1]
            # print(tmp)
            data.append(float(tmp.split(",")[0]))
            data.append(float(tmp.split(",")[1]))
            data.append(float(tmp.split(",")[2]))

    # frame x (n*3)  n is the number of sensor
    data = np.array(data).reshape(-1, 3 * nsensor)
    print(data.shape)
    return data


def read_calibrate_data(file_path):
    data = []
    with open(file_path, "rb") as f:
        i = -1
        flag = False
        nsensor = 0
        for line in f.readlines():
            i += 1
            if i == 0:
                continue
            line_decoded = line.decode("utf-8")
            if line_decoded.startswith("#"):
                if not flag and i > 1:
                    nsensor = i - 1
                    flag = True
                continue
            elif "Hz" in line_decoded:
                continue

            result = parse("X: {} 	Y: {} 	Z: {}", line_decoded)
            # print(result[0])
            data.append(float(result[0]))
            data.append(float(result[1]))
            data.append(float(result[2]))

    # frame x (n*3)  n is the number of sensor
    data = np.array(data).reshape(-1, 3 * nsensor)
    print(data.shape)
    return data


class Reading_Data(object):
    def __init__(self, data_path=None, cali_path=None):
        super().__init__()

        if data_path is not None:
            self.df = pd.read_csv(data_path)
            if "IMU" in self.df.columns:
                self.IMU = np.stack(self.df["IMU"].map(data_mapping))
                self.df = self.df.drop(["IMU"], axis=1)
            self.build_dict()
            print("Finish Loading Sensor Reading")

        if cali_path is not None:
            self.cali_data = Calibrate_Data(cali_path)
            self.calibrate()
            print("Finish Calibration")

    def build_dict(self):
        self.nSensor = len(self.df.keys()) - 2
        # old method
        old = False
        if old:
            tstamps = []
            readings = []

            results = []
            pool = Pool()

            for i in range(self.df.shape[0]):
                # self.cal_thread(i)
                results.append(pool.apply_async(self.cal_thread, args=(i,)))
            pool.close()
            pool.join()

            for result in results:
                [tstamp, readingsi] = result.get()
                tstamps.append(tstamp)
                readings.append(readingsi)

            self.tstamps = np.array(tstamps)
            self.readings = np.array(readings)

            # sort the data according the time stamp
            index = np.argsort(self.tstamps)
            self.tstamps = self.tstamps[index]
            self.readings = self.readings[index]
            self.raw_readings = self.readings.copy()
        else:
            self.tstamps = self.df["Time Stamp"].map(time_mapping).to_numpy()

            readings = []
            for i in range(self.nSensor):
                readings.append(
                    np.stack(
                        self.df["Sensor {}".format(i + 1)]
                        .map(data_mapping)
                        .to_numpy()
                    )
                )
            self.raw_readings = np.concatenate(readings, axis=1)
            self.readings = self.raw_readings.copy()

    def __len__(self):
        return self.readings.shape[0]

    def __getitem__(self, i):
        return [self.tstamps[i], self.readings[i]]

    def shape(self):
        return self.readings.shape

    def cal_thread(self, i):
        str_time = self.df["Time Stamp"][i]
        # ex. 2021-01-11 16:11:48.255801
        tdata = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S.%f")
        origin_day = datetime(year=tdata.year, month=tdata.month, day=tdata.day)
        tstamp = (tdata - origin_day).total_seconds()

        readings = []
        datai = self.df[self.df.columns[2:]].iloc[i]
        for iSensor in range(self.nSensor):
            readingi = datai["Sensor {}".format(iSensor + 1)]
            readingi = np.fromstring(readingi[1:-1], dtype=float, sep=", ")
            readings.append(readingi)

        readings = np.concatenate(readings, axis=0)

        return [tstamp, readings]

    def calibrate(self):
        [offset, scale] = self.cali_data.cali_result()
        data = self.raw_readings.copy()

        # TODO: shange mean to 50
        print(np.mean(scale))
        offset = offset.flatten()
        scale = scale.flatten()
        self.offset = offset
        self.scale = scale
        # tmp = np.mean(scale.reshape(-1, 3), axis=1, keepdims=True)
        data = (data - offset) / scale * np.mean(scale)
        # data = (data - offset) / scale * 48
        # for i in range(data.shape[1]):
        #     data[:, i] = mean_filter(data[:, i], win=3)

        self.readings = data.copy()
        # self.readings = self.readings[int(0.15 * self.readings.shape[0]
        #                                   ):int(0.99 * self.readings.shape[0])]
        # self.tstamps = self.tstamps[int(0.15 * self.tstamps.shape[0]
        #                                 ):int(0.99 * self.tstamps.shape[0])]

    def show_cali_result(self):
        self.cali_data.show_cali_result()


class Calibrate_Data:
    def __init__(self, data_path):
        super().__init__()
        self.df = pd.read_csv(data_path)
        if "IMU" in self.df.columns:
            self.df = self.df.drop(["IMU"], axis=1)
        self.build_dict()

    def build_dict(self):
        self.nSensor = len(self.df.keys()) - 2
        old = False
        if old:
            tstamps = []
            readings = []

            results = []
            pool = Pool()

            for i in range(self.df.shape[0]):
                # self.cal_thread(i)
                results.append(pool.apply_async(self.cal_thread, args=(i,)))
            pool.close()
            pool.join()

            for result in results:
                [tstamp, readingsi] = result.get()
                tstamps.append(tstamp)
                readings.append(readingsi)

            self.tstamps = np.array(tstamps)
            self.readings = np.array(readings)
            self.raw_readings = np.array(readings).copy()

            # sort the data according the time stamp
            index = np.argsort(self.tstamps)
            self.tstamps = self.tstamps[index]
            self.readings = self.readings[index]
            # print("Debug")
        else:
            self.tstamps = self.df["Time Stamp"].map(time_mapping).to_numpy()

            readings = []
            for i in range(self.nSensor):
                readings.append(
                    np.stack(
                        self.df["Sensor {}".format(i + 1)]
                        .map(data_mapping)
                        .to_numpy()
                    )
                )
            self.raw_readings = np.concatenate(readings, axis=1)
            self.readings = self.raw_readings.copy()

    def __len__(self):
        return self.readings.shape[0]

    def __getitem__(self, i):
        return [self.tstamps[i], self.readings[i]]

    def shape(self):
        return self.readings.shape

    def cal_thread(self, i):
        str_time = self.df["Time Stamp"][i]
        # ex. 2021-01-11 16:11:48.255801
        tdata = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S.%f")
        origin_day = datetime(year=tdata.year, month=tdata.month, day=tdata.day)
        tstamp = (tdata - origin_day).total_seconds()

        readings = []
        datai = self.df[self.df.columns[2:]].iloc[i]
        for iSensor in range(self.nSensor):
            readingi = datai["Sensor {}".format(iSensor + 1)]
            readingi = np.fromstring(readingi[1:-1], dtype=float, sep=", ")
            readings.append(readingi)

        readings = np.concatenate(readings, axis=0)

        return [tstamp, readings]

    def cali_result(self):
        nsensor = self.nSensor
        data = self.readings
        offX = np.zeros(nsensor)
        offY = np.zeros(nsensor)
        offZ = np.zeros(nsensor)
        scaleX = np.zeros(nsensor)
        scaleY = np.zeros(nsensor)
        scaleZ = np.zeros(nsensor)
        for i in range(nsensor):
            mag = data[:, i * 3 : i * 3 + 3]
            H = np.array(
                [
                    mag[:, 0],
                    mag[:, 1],
                    mag[:, 2],
                    -mag[:, 1] ** 2,
                    -mag[:, 2] ** 2,
                    np.ones_like(mag[:, 0]),
                ]
            ).T
            w = mag[:, 0] ** 2
            tmp = np.matmul(np.linalg.inv(np.matmul(H.T, H)), H.T)
            X = np.matmul(np.linalg.inv(np.matmul(H.T, H)), H.T).dot(w)
            # print(X.shape)
            offX[i] = X[0] / 2
            offY[i] = X[1] / (2 * X[3])
            offZ[i] = X[2] / (2 * X[4])
            temp = (
                X[5] + offX[i] ** 2 + X[3] * offY[i] ** 2 + X[4] * offZ[i] ** 2
            )
            scaleX[i] = np.sqrt(temp)
            scaleY[i] = np.sqrt(temp / X[3])
            scaleZ[i] = np.sqrt(temp / X[4])
        offset = np.stack([offX, offY, offZ], axis=0).T
        # offset = offset.reshape(1, -1)
        scale = np.stack([scaleX, scaleY, scaleZ], axis=0).T
        # scale = scale.reshape(1, -1)
        # wsy0227 save to numpy
        current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        np.save(f"mytest/offset-{current_time}.npy", offset)
        np.save(f"mytest/scale-{current_time}", scale)
        return [offset, scale]

    def show_cali_result(self):
        fig = plt.figure("Before Calibration")
        ax = fig.gca(projection="3d")
        ax.set_title("Before Calibration")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        data = self.readings
        for i in range(int(data.shape[1] / 3)):
            datai = data[:, i * 3 : i * 3 + 3]
            ax.scatter(datai[:, 0], datai[:, 1], datai[:, 2])

        fig = plt.figure("After Calibration")
        ax = fig.gca(projection="3d")
        ax.set_title("After Calibration")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        data = self.readings
        [offset, scale] = self.cali_result()
        print(offset, "\n", scale)

        offset = offset.reshape(1, -1)
        scale = scale.reshape(1, -1)
        data = self.readings
        data = (data - offset) / scale * np.mean(scale)
        # data = data.reshape(-1, 3*self.nSensor)

        for i in range(int(data.shape[1] / 3)):
            datai = data[:, i * 3 : i * 3 + 3]

            ax.scatter(datai[:, 0], datai[:, 1], datai[:, 2])

        # plt.savefig('./result/result.jpg')
        plt.show()
