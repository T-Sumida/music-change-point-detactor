# music-change-point-detactor

# Overview
SDARアルゴリズムを使った、楽曲のリアルタイム曲調変化点検知プログラム

# Environment
- Windows10 home 64bit
- CUDA 10.1
- wsl2(Docker)

1. Dockerイメージの作成
    ```
    docker build -t {イメージ名} -f /path/to/Dockerfile .
    ```
2. Dockerコンテナの作成
    ```
    docker run --gpus all --ipc=host --rm -p 8888:8888 -it -v /path/to/this/repository/folder:/work {イメージ名}
    ```

# Usage
### マイク入力（リアルタイム）で動作させる場合
1. settings.yamlのdev_idとchannelを適切に設定する
2. ```$ python app.py``` を実行する

### オーディオファイルで動作させる場合
1. ```$ python app.py --file {オーディオファイルのパス}``` を実行する




# Task
- change_finderを用いる場合、パラメータの調整を適切にする必要がある
- 検証した楽曲数が少ないため、より多くの楽曲で検証する必要がある

# License
Copyright © 2020 T_Sumida Distributed under the MIT License.