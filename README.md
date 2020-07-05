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
工事中

# License
Copyright © 2020 T_Sumida Distributed under the MIT License.