import json
import os
import re

import cv2
import requests

from app_ui import App

head_list = {
    "Host": "bbs-api.miyoushe.com",
    "Origin": "https://m.miyoushe.com",
    "Referer": "https://m.miyoushe.com/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"
}


def detect(filename, cascade_file="lbpcascade_animeface.xml"):
    if not filename.endswith(".gif"):
        cascade = cv2.CascadeClassifier(cascade_file)
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(24, 24))
        return len(faces) > 0
    return True
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #
    # cv2.imshow("AnimeFaceDetect", image)
    # cv2.waitKey(0)
    # cv2.imwrite("out.png", image)


class ImgBean:
    name = ""
    img_bean = ""

    def __init__(self, name, img_url):
        self.name = name
        self.url = img_url


def extract_img_url(text):
    pattern = r'<img src="([^"]+)"'
    match = re.search(pattern, text)
    if match:
        url = match.group(1)
        return url
    else:
        return None


image_beans = []


def request_content(last_id):
    _url = f"https://bbs-api.miyoushe.com/post/wapi/getPostReplies?gids=2&is_hot=true&only_master=false&post_id={app.get_post_id()}&size=20&last_id={last_id}"
    app.output_log(_url)
    json_text = requests.get(_url, headers=head_list).text

    json_obj = json.loads(json_text)
    if not json_obj.get("data").get("is_last"):
        request_content(json_obj.get("data").get("last_id"))
    json_arr = json_obj.get("data").get("list")
    for obj in json_arr:
        img_arr = obj.get("images")
        if len(img_arr) > 0:
            for img in img_arr:
                image_beans.append(ImgBean(img.get("entity_id"), img.get("url")))


def download(img_url):
    app.output_log(f"{img_url} is downloading...")
    return requests.get(img_url, stream=True)


def save_file(folder_name, img_file, file_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    with open(f"{folder_name}/{file_name}", "wb") as f:
        for chunk in img_file.iter_content(chunk_size=512):
            f.write(chunk)


def start():
    post_id = app.get_post_id()
    folder = f"{app.folder_path}/miyoushe/data/{post_id}"
    if not post_id:
        app.output_log("请输入post_id")
        return
    if not folder:
        app.output_log("请选择要保存的目录")
        return
    folder = f"C:\\Users\\59432\\PycharmProjects\\miyoushe\\data\\{post_id}"
    request_content(0)

    for img_bean in image_beans:
        img = download(img_bean.url)
        save_file(folder, img, f"{img_bean.name}{os.path.splitext(str(img_bean.url))[-1]}")
    if app.get_filter_checked() == 1:
        remove_not_2d_character(folder)


def remove_not_2d_character(folder):
    for f in os.listdir(folder):
        file_name = f"{folder}\\{f}"
        if not detect(file_name):
            os.remove(file_name)
            app.output_log(f"{file_name} has removed.")


if __name__ == '__main__':
    app = App()
    app.start = start
    app.create_window()
