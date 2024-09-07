# PagerMaidPyro\_Plugins

PagerMaidPyro\_Plugins 是一个为 PagerMaid\_Pyro 提供的自定义插件库。通过添加自定义仓库，实现插件的分发和下载。

## 功能

- 列出可用插件
- 从 GitHub 仓库下载插件
- 缓存插件版本以加快访问速度

## 依赖

见 `requirements.txt`

## 安装

1. 克隆仓库：
    ```sh
    git clone https://github.com/yourusername/PagerMaidPyro_Plugins.git
    cd PagerMaidPyro_Plugins
    ```

2. 安装所需的包：
    ```sh
    pip install -r requirements.txt
    ```

## 配置

编辑 `config.toml` 文件以添加自定义仓库和插件。示例：

```toml
[app]
ip = "127.0.0.1"
port = 3526

[plugins.chouxiang]
description = "抽象语录"
repo = "sahuidhsu/PM_chouxiang"
file = "chouxiang_pyro.py"