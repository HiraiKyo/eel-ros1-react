#!/usr/bin/env python
# mypy: ignore-errors

import os
import sys
import eel
from jinja2 import Environment, FileSystemLoader
import rospkg
import argparse
import rospy

# Actionsをインポートして、このファイルにバンドルする
from eel_ros1.actions import *  # noqa: F403
from eel_ros1.models import ros_service, rosparam # FIXME: おそらくros_serviceのインポートはここ必須
from eel_bundler.main import bundle

PACKAGE_NAME = "eel_ros1"
Config = ros_service.Config
OPTIONS = {
    "host": "0.0.0.0",
    "port": 8000,
    'cmdline_args': ["--no-sandbox"],
    'size': (800, 600),
    # "block": False
}

# Jinja2の設定
rospack = rospkg.RosPack()
package_path = rospack.get_path(PACKAGE_NAME)
abs_path = os.path.join(package_path, 'templates')

# コマンドライン引数の処理
argv = rospy.myargv(argv=sys.argv)
parser = argparse.ArgumentParser(description="EEL Example")
parser.add_argument("--html_dir", help="HTML directory path")
parser.add_argument("--port", help="Port number")
args = parser.parse_args(argv[1:])
if args.html_dir:
    abs_path = args.html_dir
if args.port:
    OPTIONS['port'] = args.port

if __name__ == '__main__':
    dist_path = bundle(package_path, template=abs_path)
    print("Starting Eel app...")
    print("  dist path: ", dist_path)
    print("  hosted at:", f"http://{OPTIONS['host']}:{OPTIONS['port']}")
    eel.init(dist_path)
    rosparam.run_getparam_loop()
    eel.start('index.html', **OPTIONS)

    rosparam.break_getparam_loop()
    print("[CA] App quitted.")
    sys.exit()