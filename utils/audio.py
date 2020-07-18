# coding: utf-8

import sys
import queue
from typing import Dict
import sounddevice as sd


class Audio(object):
    ERROR = -1
    SUCCESS = 1
    WAIT = 0

    def __init__(self, cfg: Dict, audio_file_path: str = None):
        """コンストラクタ

        Args:
            cfg (Dict): 設定情報
            audio_file_path (str, optional): 音楽ファイルパス. Defaults to None.
        """
        self.cfg = cfg
        self.q = None
        if audio_file_path is not None:
            self._init_local(audio_file_path)
            self.get = self._get_from_local
        else:
            self._init_realtime()
            self.get = self._get_from_stream

    def _init_local(self, audio_file_path: str):
        """音楽ファイル用の初期化

        Args:
            audio_file_path (str): 音楽ファイルパス
        """
        import librosa
        self.data, sr = librosa.load(
            audio_file_path,
            sr=self.cfg['sr'],
            mono=True
        )

        self.max_counter = range(
            0, self.data.shape[0], self.cfg['block_size']
        )[-1]
        self.counter = -self.cfg['block_size']

    def _init_realtime(self):
        """リアルタイム処理用ストリームの初期化 """
        info = sd.query_devices(device=int(self.cfg['dev_id']), kind='input')
        print(info)

        self.stream = sd.InputStream(
            device=self.cfg['dev_id'],
            channels=self.cfg['chennel'],
            samplerate=self.cfg['sr'],
            blocksize=self.cfg['block_size'],
            callback=self._audio_callback
        )
        self.q = queue.Queue()
        self.status = Audio.SUCCESS

    def start(self):
        """ストリーミング開始"""
        if self.q is None:
            return
        self.q.queue.clear()
        self.stream.start()

    def stop(self):
        """ストリーミング停止"""
        if self.q is None:
            return
        self.stream.stop()

    def _get_from_local(self):
        """音楽ファイルから指定されたサイズ・スライド幅でデータを返す

        Returns:
            numpy.array -- 信号
        """
        self.counter += self.cfg['block_size']
        if self.counter > self.max_counter:
            return Audio.ERROR, 0
        return Audio.SUCCESS, self.data[self.counter:self.counter+self.cfg['block_size']]

    def _get_from_stream(self):
        """マイク入力から指定されたサイズ・スライド幅でデータを返す

        Returns:
            numpy.array -- 信号
        """
        try:
            data = self.q.get_nowait()
        except Exception as e:
            print(e)
            return Audio.WAIT, None

        return self.status, data

    def _audio_callback(self, indata, frames, time, status):
        """信号入力用コールバック

        Arguments:
            indata {numpy.array} -- 信号
            frames {int} -- 信号のサイズ
            time {CData} -- ADCキャプチャ時間
            status {CallbackFlags} -- エラー収集用のフラグ
        """
        if status:
            print("[audio callback error] {}".format(status))
            print(status, file=sys.stderr)
            # self.status = Audio.ERROR
        self.q.put(indata[:, self.channels-1])
