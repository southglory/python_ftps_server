# server.py
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
from pyftpdlib.servers import FTPServer
import os

# 사용자 인증 설정
authorizer = DummyAuthorizer()
authorizer.add_user("user", "password", os.path.abspath("ftp_root"), perm="elradfmwMT")

# FTPS 핸들러 설정
handler = TLS_FTPHandler
handler.certfile = "cert.pem"
handler.keyfile = "key.pem"
handler.authorizer = authorizer
handler.tls_control_required = True
handler.tls_data_required = True
handler.passive_ports = range(60000, 60010)  # 파이어월 피해서 Passive 모드 설정

# 서버 생성
server = FTPServer(("0.0.0.0", 2121), handler)
print("✅ FTPS 서버 실행 중! 포트: 2121")
server.serve_forever()
