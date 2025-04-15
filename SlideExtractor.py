import os
import requests
from tqdm import tqdm

from SlideDetector import video2slide


def download(url):
    res = requests.get(url, stream=True) # 设定为流
    total_size = int(res.headers.get("Content-Length", 0)) # 文件总大小
    block_size = 1024 # 每次迭代下载大小
    progress_bar = tqdm(total = total_size, unit='iB', unit_scale=True)
    filename = os.path.join(os.getcwd(), "./videos/screen.mp4")
    with open(filename, "wb") as f:
        for data in res.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
        progress_bar.close()
    print("下载完成")


if __name__ == '__main__':
    # 在这这里放置你的课程编号
    course_id = "24916"

    # 在这里放置你的session Cookie
    session = ""


    url = "https://ispace.xjtu.edu.cn/api/course/"+course_id+"/coursewares"

    headers = {"Cookie" : "session=" + session}

    params = {"conditions" : '{"category":"lesson","itemsSortBy":{"predicate":"chapter","reverse": "false"}}', "page" : "1", "page_size" : 100}

    result = requests.get(url, headers=headers, params=params)

    json = result.json()

    print(len(json["activities"]))
    lesson_count = len(json["activities"])
    lesson_current = 0

    for item in reversed(json["activities"]):
        if os.path.exists("./output/" + str(lesson_current) + ".pdf"):
            lesson_current = lesson_current + 1
            continue
        id = item["id"]
        url = "https://ispace.xjtu.edu.cn/api/activities/"+str(id)
        result = requests.get(url, headers=headers)
        json = result.json()
        url = json["video_suite"]["videos"][1]["file_url"]
        print("Downloading", lesson_current, "/", lesson_count, "lessons.")
        download(url)

        print("Extracting Slides...")
        video2slide(str(lesson_current))
        print("Done.")

        # video2slide(str(lesson_current))
        lesson_current = lesson_current + 1