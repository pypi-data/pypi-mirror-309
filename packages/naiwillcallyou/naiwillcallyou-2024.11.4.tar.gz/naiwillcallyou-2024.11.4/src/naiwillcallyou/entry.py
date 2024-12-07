import json
import os
import requests


def main():
    config_path = os.path.join(os.path.expanduser("~"), ".naiwillcallyou.json")
    
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            json.dump({"name": "", "msg": ""}, f)
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    name = config["name"]
    msg = config["msg"]
    
    if not name or not msg:
        print("Please set your name and message in ~/.naiwillcallyou.json first!")
        return
    
    response = requests.get(f"http://emeryville.asuscomm.com:8066/wechat/send?name={name}&msg={msg}")
    # print(response.text)


if __name__ == "__main__":
    main()

