# !/usr/bin/env python3
        "scene": "link",
    }
    headers = common_headers()
    response = requests.request(
        "POST", url, json=payload, headers=headers, params=querystring
    ).json()
    return response


def mkdir(dir_path):
    url = "https://drive-pc.quark.cn/1/clouddrive/file"
    querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
    payload = {
        "pdir_fid": "0",
        "file_name": "",
        "dir_path": dir_path,
        "dir_init_lock": False,
    }
    headers = common_headers()
    response = requests.request(
        "POST", url, json=payload, headers=headers, params=querystring
    ).json()
    return response["data"]


def rename(fid, file_name):
    url = "https://drive-pc.quark.cn/1/clouddrive/file/rename"
    querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
    payload = {"fid": fid, "file_name": file_name}
    headers = common_headers()
    response = requests.request(
        "POST", url, json=payload, headers=headers, params=querystring
    ).json()
    return response["data"]

def query_update_list():
    url = "https://drive-pc.quark.cn/1/clouddrive/share/update_list"
    querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
    payload = {
        "page": 1,
        "needTotalNum": 1,
        "share_read_statues": [
            0,
            1
        ],
        "fetch_total": 1,
        "fetch_max_file_update_pos": 1,
        "fetch_update_files": 1,
        "page_size": 100
    }
    headers = common_headers()
    response = requests.request(
        "POST", url, json=payload, headers=headers, params=querystring
    ).json()
    return response["data"]["list"]

def format_sublist(sublist):
    subtasklist = []
    for sublistitem in sublist:
        if sublistitem["save_as_status"] == 0:
            share_url = f"{sublistitem['share_url']}?read=1&passcode=#/list/share/{sublistitem['first_fid']}-{sublistitem['title']}"
            subtasklist.append({
                "taskname": sublistitem["title"],
                "shareurl": share_url,
                "savepath": "/动漫",
                "pattern": "\\.(mp4|mkv)$",
                "replace": "",
                "enddate": "",
                "emby_id": "",
                "savepath_fid": "2f4287e257c2429ba63f40fbfa10eb86"
            })
    return subtasklist

def update_savepath_fid(tasklist):
    dir_paths = [
        item["savepath"]
        for item in tasklist
        if not item.get("enddate")
        or (
            datetime.now().date()
            <= datetime.strptime(item["enddate"], "%Y-%m-%d").date()
        )
    ]
    dir_paths_exist_arr = get_fids(dir_paths)
    dir_paths_exist = [item["file_path"] for item in dir_paths_exist_arr]
    # 比较创建不存在的
    dir_paths_unexist = list(set(dir_paths) - set(dir_paths_exist))
    for dir_path in dir_paths_unexist:
        new_dir = mkdir(dir_path)
        dir_paths_exist_arr.append({"file_path": dir_path, "fid": new_dir["fid"]})
