import json
import time
import requests


class PublicIPTracker:
    def __init__(self):
        """ "
        初始化PublicIPTracker类
        1. 获取公网IP地址
        2. 获取公网IP的详细信息
        3. 将日志发送到指定的URL
        """
        self.public_ip = None
        self.ip_details = None

    def get_public_ip(self):
        """获取公网IP地址"""
        try:
            response = requests.get("https://httpbin.org/ip")
            self.public_ip = response.json()["origin"]
            return self.public_ip
        except requests.RequestException as e:
            print(f"获取公网IP失败: {e}")
            return None

    def get_public_ip_details(self):
        """获取公网IP的详细信息"""
        if self.public_ip is None:
            self.get_public_ip()
        try:
            url = (
                f"https://qifu-api.baidubce.com/ip/geo/v1/district?ip={self.public_ip}"
            )
            response = requests.get(url)
            self.ip_details = response.json()
            return self.ip_details
        except requests.RequestException as e:
            print(f"获取公网IP详细信息失败: {e}")
            return None

    def track_log(self):
        """将日志发送到指定的URL"""
        if self.ip_details is None:
            self.get_public_ip_details()
        if self.ip_details is None:
            return None
        url = "https://ap-shanghai.cls.tencentcs.com/tracklog?topic_id=af66262a-df31-4567-9ac0-bf822d62e076"
        headers = {
            "Content-Type": "application/json",
            "Host": "ap-shanghai.cls.tencentcs.com",
        }
        current_timestamp = int(time.time())
        new_data = {
            "logs": [
                {
                    "contents": {
                        "id": current_timestamp,
                        "continent": self.ip_details.get("data", {}).get("continent"),
                        "country": self.ip_details.get("data", {}).get("country"),
                        "zipcode": self.ip_details.get("data", {}).get("zipcode"),
                        "owner": self.ip_details.get("data", {}).get("owner"),
                        "isp": self.ip_details.get("data", {}).get("isp"),
                        "adcode": self.ip_details.get("data", {}).get("adcode"),
                        "prov": self.ip_details.get("data", {}).get("prov"),
                        "city": self.ip_details.get("data", {}).get("city"),
                        "district": self.ip_details.get("data", {}).get("district"),
                        "ip": self.public_ip,
                        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    },
                    "time": current_timestamp,
                }
            ],
            "source": self.public_ip,
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(new_data))
            return response.json()
        except requests.RequestException as e:
            print(f"发送日志失败: {e}")
            return None
