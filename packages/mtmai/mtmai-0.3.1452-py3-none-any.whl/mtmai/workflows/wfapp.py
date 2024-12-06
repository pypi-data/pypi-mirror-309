import os

from dotenv import load_dotenv
from mtmaisdk import ClientConfig, Hatchet

load_dotenv()


# 不验证 tls 因后端目前 证数 是自签名的。
os.environ["HATCHET_CLIENT_TLS_STRATEGY"] = "none"
os.environ["HATCHET_CLIENT_TOKEN"] = (
    "eyJhbGciOiJFUzI1NiIsICJraWQiOiJqX3dWMGcifQ.eyJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgwODAiLCAiZXhwIjo0ODg1MjQ4MzE2LCAiZ3JwY19icm9hZGNhc3RfYWRkcmVzcyI6ImxvY2FsaG9zdDo3MDc3IiwgImlhdCI6MTczMTY0ODMxNiwgImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODA4MCIsICJzZXJ2ZXJfdXJsIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwIiwgInN1YiI6IjMxMjcxMWY0LWRlZmQtNGEwMy05NWE2LTg4MjY1NmNlODA4MiIsICJ0b2tlbl9pZCI6IjEzMDFkNmVlLTAxNDctNDk1Ny05NWJjLTViODcyOTQzYmE5MCJ9.6xYZM0oORYeSTSzRzC_CU8UKQd_p4JHj_wdthLY0CHYelZGWFSsgpChn1MXSPnJ5f1SF6h-eMlWnsQgnoVluRw"
)


server_url = "http://localhost:8383"
wfapp = Hatchet(
    debug=True,
    config=ClientConfig(
        server_url=server_url,
    ),
)
