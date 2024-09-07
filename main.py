import logging
import os
from traceback import print_exc

import requests
import toml
from diskcache import Cache
from flask import Flask, jsonify, abort, send_file

DATA_DIR = "data"

logger = logging.getLogger()
logger.setLevel("INFO")
BASIC_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()
chlr.setFormatter(formatter)
logger.addHandler(chlr)

# 读取配置文件
config = toml.load('config.toml')
cache = Cache()
app = Flask(__name__)

# 插件列表
plugins = config['plugins']
os.makedirs(DATA_DIR, exist_ok=True)


def get_version(repo):
    # 从缓存中读取版本号
    version = cache.get(f"version_{repo}")
    if version is None:
        try:
            # 从GitHub获取最新版本号
            res = requests.get(f"https://api.github.com/repos/{repo}/releases/latest",
                               headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code != 200:
                logger.error(f"获取插件{repo}版本号失败，状态码：{res.status_code}")
                return None
            version = res.json()['tag_name']
            cache.set(f"version_{repo}", version, 300)
            logger.info(f"获取插件{repo}版本号成功")
        except:
            print_exc()
            logger.error(f"获取插件{repo}版本号失败")
            return None
    return version


@app.route('/list.json', methods=['GET'])
def list_plugins():
    logger.info("获取插件列表")
    result = {"list": []}
    for item in plugins:
        data = {
            "name": item,
            "des": plugins[item]['description'],
            "des_short": plugins[item]['description'],
            "section": "",
            "maintainer": "",
            "version": get_version(plugins[item]['repo']),
            "supported": True,
            "size": ""
        }
        result['list'].append(data)
    # 构建 JSON 响应
    return jsonify(result)


@app.route('/<plugin>/main.py', methods=['GET'])
def download_plugin(plugin):
    logger.info(f"下载插件 {plugin}")
    if plugin not in plugins:
        logger.error(f"插件 {plugin} 不存在")
        abort(404, description=f"插件 {plugin} 不存在")

    repo = plugins[plugin]['repo']
    file_path = plugins[plugin]['file']
    version = get_version(repo)
    if not version:
        abort(500, description="无法获取插件版本号")

    local_file = f"{DATA_DIR}/{plugin}-{version}.py"

    if not os.path.exists(local_file):
        logger.info(f"本地文件 {local_file} 不存在，开始从 GitHub 下载")
        raw_url = f"https://raw.githubusercontent.com/{repo}/main/{file_path}"
        res = requests.get(raw_url)
        if res.status_code == 200:
            with open(local_file, 'wb') as f:
                f.write(res.content)
            logger.info(f"插件 {plugin} 下载成功")
        else:
            logger.error(f"下载插件 {plugin} 失败，状态码：{res.status_code}")
            abort(500, description="下载插件失败")

    return send_file(local_file, download_name="main.py")


if __name__ == '__main__':
    ip = config['app']['ip']
    port = config['app']['port']
    app.run(host=ip, port=port)
