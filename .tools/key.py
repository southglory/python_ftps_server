from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, UTC

# 1. 비밀 키 생성
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 2. 인증서 주체 정보
subject = issuer = x509.Name(
    [
        x509.NameAttribute(NameOID.COUNTRY_NAME, "KR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Seoul"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Seoul"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Quirka Games"),
        x509.NameAttribute(NameOID.COMMON_NAME, "quirkagames.com"),
    ]
)

now = datetime.now(UTC)

# 3. SAN에 들어갈 여러 도메인
alt_names = [
    x509.DNSName("quirkagames.com"),
    x509.DNSName("www.quirkagames.com"),
    x509.DNSName("dev.quirkagames.com"),
    x509.DNSName("api.quirkagames.com"),
    x509.DNSName("staging.quirkagames.com"),
    x509.DNSName("localhost"),
]

# 4. 인증서 빌드
cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now)
    .not_valid_after(now + timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName(alt_names),
        critical=False,
    )
    .sign(key, hashes.SHA256())
)

# 5. 파일로 저장
with open("key.pem", "wb") as f:
    f.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ 인증서가 다음 도메인으로 생성되었습니다:")
for name in alt_names:
    print(" -", name.value)
