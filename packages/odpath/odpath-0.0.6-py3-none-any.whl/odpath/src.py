import os
import os.path as osp

import cv2


# 获取常用的图片后缀
def get_img_ext():
    ext = [
        ".bmp",
        ".dng",
        ".jpeg",
        ".jpg",
        ".mpo",
        ".png",
        ".tif",
        ".tiff",
        ".webp",
        ".pfm",
    ]
    # 获取大写的后缀
    ext.extend([e.upper() for e in ext])
    return ext


def find_files(
    directory, pattern=None, contains=None, onlyfirst=True, onlyimg=True, display=True
):
    filepath_list = []
    filename_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if contains is not None and file.find(contains) == -1:
                continue
            ext = file[file.rfind(".") :].lower()

            # 只获取指定后缀的文件
            if pattern is not None:
                if isinstance(pattern, str) and not ext.endswith(pattern):
                    continue
                if isinstance(pattern, list) and ext not in pattern:
                    continue

            # 只获取图片格式文件
            if onlyimg and ext not in get_img_ext():
                continue

            filepath = os.path.join(root, file)
            # 统一路径格式，统一使用/
            filepath = filepath.replace("\\", "/")
            filepath_list.append(filepath)
            filename_list.append(file)
        if onlyfirst:
            break
    # 控制是否打印
    if display:
        print("total number of files: %d" % len(filepath_list))
    return filepath_list, filename_list


def get_files_path(
    input_file, pattern=None, contains=None, onlyfirst=True, onlyimg=True, display=True
):
    """
    在指定目录下查找文件，并根据指定的条件过滤文件。
    参数:
        directory (str): 要搜索的目录路径。
        pattern (str or list, optional): 文件扩展名模式，可以是字符串或字符串列表。默认为 None。
        contains (str, optional): 文件名中必须包含的字符串。默认为 None。
        onlyfirst (bool, optional): 是否只搜索目录的第一级。默认为 True。
        onlyimg (bool, optional): 是否只搜索图片文件。默认为 True。
        display (bool, optional): 是否显示搜索结果。默认为 True。
    返回:
        tuple: 包含符合条件的文件路径列表和文件名列表的元组。
    """
    if input_file and os.path.isfile(input_file):
        imgpath = osp.abspath(input_file)
        imgname = osp.basename(input_file)
        return [imgpath], [imgname]

    infer_dir = os.path.abspath(input_file)
    assert os.path.isdir(infer_dir), "{} is not a directory".format(infer_dir)
    img_paths, img_names = find_files(
        input_file, pattern, contains, onlyfirst, onlyimg, display
    )
    return img_paths, img_names


def get_folders_path(directory, contains=None, onlyfirst=True, display=True):
    """
    在指定目录下查找文件夹，并根据指定的条件过滤文件夹。
    参数:
        directory (str): 要搜索的目录路径。
        contains (str, optional): 文件夹名中必须包含的字符串。默认为 None。
        onlyfirst (bool, optional): 是否只搜索目录的第一级。默认为 True。
        display (bool, optional): 是否显示搜索结果。默认为 True。
    返回:
        tuple: 包含符合条件的文件夹路径列表和文件夹名列表的元组。
    """
    folderpath_list = []
    foldername_list = []
    for root, dirs, _ in os.walk(directory):
        for folder in dirs:
            if contains is not None and folder.find(contains) == -1:
                continue
            folderpath = os.path.join(root, folder)
            # 统一路径格式，统一使用/
            folderpath = folderpath.replace("\\", "/")
            folderpath_list.append(folderpath)
            foldername_list.append(folder)
        if onlyfirst:
            break
    # 控制是否打印
    if display:
        print("total number of folders: %d" % len(folderpath_list))
    return folderpath_list, foldername_list


# 展示图片
def show(img, win_name="image", time=0):
    cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
    cv2.imshow(win_name, img)
    if time >= 0:
        cv2.waitKey(time)


# 把点值int化
def int_pt(pt):
    int_pt = (int(pt[0]), int(pt[1]))
    return int_pt


if __name__ == "__main__":
    inputpath = (
        r"E:\ODProjects\Datasets\od_data_pyqt\datasets\yb_85_426\images_20240925"
    )
    # img_paths, img_names = get_files_path(
    #     inputpath, onlyimg=True, onlyfirst=False, pattern=[".jpg", ".json"]
    # )

    folders = get_folders_path(inputpath, onlyfirst=False, contains="D")

    print(folders)
