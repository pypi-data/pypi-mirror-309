import os

from dotenv import load_dotenv
from mtmaisdk import ClientConfig, Hatchet
from mtmai.core.config import settings

load_dotenv()

# 不验证 tls 因后端目前 证数 是自签名的。
os.environ["HATCHET_CLIENT_TLS_STRATEGY"] = "none"
os.environ["HATCHET_CLIENT_TOKEN"] = settings.HATCHET_CLIENT_TOKEN
wfapp = Hatchet(
    debug=True,
    config=ClientConfig(
        # 提示 client token 本身已经包含了服务器地址（host_port）信息
        server_url=settings.GOMTM_URL,
    ),
)
