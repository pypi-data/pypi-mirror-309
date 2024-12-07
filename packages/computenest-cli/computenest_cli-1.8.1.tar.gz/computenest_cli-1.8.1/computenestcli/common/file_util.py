import os
import shutil

exclude_dirs = ['.git', '.idea', '.vscode', '.DS_Store', '__pycache__']


class FileUtil:
    def __init__(self):
        pass

    @staticmethod
    def remove_subdirectories(directories):
        # 将目录列表先排序，以便父目录出现在前面
        sorted_dirs = sorted(directories)

        # 储存父目录的集合
        filtered_dirs = set()

        for dir_path in sorted_dirs:
            # 检查当前目录是否是已经在集合中的任何父目录的子目录
            if not any(dir_path.startswith(parent_dir + '/') for parent_dir in filtered_dirs):
                filtered_dirs.add(dir_path)

        return filtered_dirs

    @staticmethod
    def copy_excluding_directory(src, dest, exclude_dir):
        # 创建目标目录
        if not os.path.exists(dest):
            os.makedirs(dest)

        if not os.path.exists(src):
            os.makedirs(os.path.join(dest, os.path.relpath(src, os.getcwd())), exist_ok=True)
            return

        # 对于是src_dir为命令执行的根目录情况，需要跳过部分文件
        if src == os.getcwd():
            for item in os.listdir(src):
                s_item = os.path.join(src, item)
                d_item = os.path.join(dest, item)
                # 跳过部分指定目录
                if item in exclude_dirs:
                    continue
                if os.path.isdir(s_item) and not os.path.commonpath([s_item]) == os.path.commonpath(
                        [s_item, exclude_dir]):
                    shutil.copytree(s_item, d_item, dirs_exist_ok=True)
                    continue
                elif os.path.isfile(s_item):
                    shutil.copy2(s_item, d_item)
            return

        # 对于其他情况，直接复制
        dest = os.path.join(dest, os.path.relpath(src, os.getcwd()))

        if not os.path.exists(src) or not os.listdir(src):
            os.makedirs(dest, exist_ok=True)
            return

        if os.path.isdir(src):
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dest)
