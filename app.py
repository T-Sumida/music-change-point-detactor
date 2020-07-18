# coding: utf-8
import argparse

import yaml
import librosa
import numpy as np
import changefinder as cf

from utils.audio import Audio


class MusicChangePointDetector(object):
    def __init__(self, setting_path: str, audio_path: str):
        """コンストラクタ

        Args:
            setting_path (str): 設定ファイルのパス
            audio_path (str): 音楽ファイルのパス
        """
        with open(setting_path, 'r') as f:
            cfg = yaml.load(f)

        self.cf = cf.ChangeFinder(**cfg['change_finder'])
        self.audio = Audio(cfg['audio'], audio_file_path=audio_path)

        self.buffer = np.zeros(
            cfg['model']['buffer_audio_length'], dtype=np.float32
        )
        self.buf_num = int(cfg['model']['frame_buf_num'])
        self.spec_buf = []
        self.thr = float(cfg['model']['thr'])

    def run(self):
        """メインループ開始"""
        self.audio.start()
        try:
            while True:
                status, data = self.audio.get()

                if status == Audio.ERROR:
                    break
                elif status == Audio.WAIT:
                    continue

                self.buffer = np.roll(self.buffer, -data.shape[0], axis=0)
                self.buffer[-data.shape[0]:] = data

                if self.detect():
                    print('detect')

        except KeyboardInterrupt:
            print('Interrupt')
        self.audio.stop()

    def detect(self):
        """検出

        Returns:
            bool: 転調したかどうか
        """
        is_detect = False
        D = np.average(
            librosa.amplitude_to_db(
                np.abs(librosa.stft(self.buffer)), ref=np.max
            ), axis=1
        )[:512]
        D /= np.linalg.norm(D, ord=2)
        self.spec_buf.append(D)

        if len(self.spec_buf) > self.buf_num:
            similarity = np.average(
                np.dot(
                    self.spec_buf[-1], np.array(self.spec_buf[-(self.buf_num-1):-1]).T
                )
            )
            score = self.cf.update(similarity)
            self.spec_buf.pop()
            if score > self.thr:
                is_detect = True

        return is_detect


def get_args():
    """引数解析

    Returns:
        argparse.Namespace: 引数情報
    """
    parser = argparse.ArgumentParser(
        prog="app.py",
        usage="realtime or audio file",
        description="detect music change point.",
        add_help=True
    )

    parser.add_argument(
        "--cfg", type=str,
        default="./settings.yaml",
        help="setting file path"
    )
    parser.add_argument(
        "--file", type=str,
        default=None,
        help="audio file path"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    detector = MusicChangePointDetector(args.cfg, args.file)

    detector.run()
