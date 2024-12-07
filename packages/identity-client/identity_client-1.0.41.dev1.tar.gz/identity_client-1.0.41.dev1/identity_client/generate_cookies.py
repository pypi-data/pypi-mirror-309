import time
from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime

resource = "designhub-staging/assets/models/08-22T10-26-50-955973/test-bw_4Colorway_1_front.png"
domain = "assets-v2.hub3d.pvh.com"
key_pair_id = "APKAJ7ISVY5AQEUUMLRQ"
PRIVATE_KEY_RAW = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAhrjMlSx9zztdaHmXqUSSHVVDnvd4qBBiypTjGMUb9/yzUaGQ
X4XYrMq25MJqLmcBPRGQ0R66Hj1IJ1PONNYXeRgiVnsj7ojFswDR/+PwZrTFXfQ9
F92FUQSSc9m+iCzvw/cpCJieBhGagJFv6ymOE9Q134DRNJ4ybtX4KUzcj1R1QDx7
/csyb7vUmElwBgA1ddz3qYx6K36OxnUpV6ck2p2r3KtpRZHBP/J5yK6UttdAr6D8
Sft5mJCWmJwbebJYpXDorsM6mnBaVCHD/tARWu1JU/B4C9ihyBy8NSH9eNZ38oUU
Y9tOh0/wZCFN0dFSYSK3r08JO5DBVRGAwHOXhQIDAQABAoIBAANJePxexIcM3L+S
z+d6W9JJZUf4o8H9/FsS/ON6067eRIXGWl5qRpoYrBOyxqJxMu+JgS4JAOOB/UOw
YMSbQKFcvGG9yWelgKVYbMdAiXoICRS8w8zUQ89xPB2Ff4eVCRiP7Dlgd+KQBWQD
qGZlcij7sYDNhM0y2uonYFGppWv9y3pCz5qRsqSvjtGaejQYRUMDRxhntC78Hmhc
IXNe43sMNSi+OufSsH2/wwixByLD3OUwqQvCfXJj936+TVSszKhvaAA8oQ2svRLM
tCfjMnfNdnaF+KuEcSMVrcJ7yVLF3UQa1JOHfVz7bmM6JukX4hhzy558B1ArtZvr
pnb/nHUCgYEAvQN2c2lv4bxPSY9HM1MM7tWeGoB0dlHNkOVRpx/cTR20rocWs2yv
C72CJ52xpRijO7U+D65y26yv9qGqhFV/qHuwtEBI7s1Zup9FJHmQ5kqL0SVxH9Dj
HDEI6MhLv5UjELF7MCBaA3PWAYB4Win3I0YrFx6HSSOFdMDOouY57t8CgYEAtnek
6hmC/G1EmPAlVHZbSKlx6yPXuH450H6XSpU8iZ6Kf1frinObagg97JeGplNGzjci
r7PIdrdMY/k3s82QIh3ko0cm/2J+uq1fbphm+enOxnkI1vOJWXpy80JSq6Dotd49
0KyFJyNb72yehfKm6/g+OEusZ9jNDjMJ+CpDWhsCgYBh0PTv7VTVQZrWuqtiSEyd
HTfhBzE+Oj9kCQkksDxWPFVRLN/2ovxD2yMMVXOluQZg0/72JpWSUeAOhsO0EHss
OjbMUahszSDuj5Y8thzi0Rlidzn/+R5PbKDrtxxcXVX0QaU61sM+nifWRyIBp04a
lymdoVLp6tQaA93sN7EriQKBgAV7aMADzjSpT8NMi8KS38E6HgsTg5quaCxEcWUz
QKNd2QlkadY6DPRNlRazor8Ch4EQlQE0ZJR0g14JkcvcJDVyMnlZXOmVWvte1Bwt
hgKCLM03u7VBkeHXVPbMClHPvs4gBDltxX5ciJmT6NtbY/p49d2ZIG/qSpbfn7AO
DQH7AoGBALujvRxQAQlOrKps5pjWTHPiQ9bhDvVPCOe1V51uX6qKak2IIm2we3oy
tmIXcJYswMgeGkTG2+miCnYmUTYAi9+ZNYPlw+2eiHI0u40iGfiwj3eq6x8XZzOo
Vpi28LXrYopDeOkhsVDEVDdIzXWwiHOHyIoxA0g35yKX2ZQjxF96
-----END RSA PRIVATE KEY-----"""
private_key = serialization.load_pem_private_key(
    PRIVATE_KEY_RAW.encode("utf-8"), password=None, backend=default_backend()
)


def rsa_signer(message):
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def get_http_resource_url(resource=None, secure=False):
    """
    @resource   optional path and/or filename to the resource
                (e.g. /mydir/somefile.txt);
                defaults to wildcard if unset '*'
    @secure     whether to use https or http protocol for Cloudfront URL - update
                to match your distribution settings
    return constructed URL
    """
    if not resource:
        resource = "*"
    protocol = "http" if not secure else "https"
    http_resource = "%s://%s/%s" % (protocol, domain, resource)
    return http_resource


http_resource = get_http_resource_url(
    resource, secure=True
)  # per-file access #NOTE secure should match security settings of cloudfront distribution
cloudfront_signer = CloudFrontSigner(key_pair_id, rsa_signer)
expires = int(time.time() + (3 * 60))
policy = cloudfront_signer.build_policy(http_resource, datetime.fromtimestamp(expires))
encoded_policy = cloudfront_signer._url_b64encode(policy.encode("utf-8")).decode(
    "utf-8"
)
# Add these lines after policy is created but before encoding
print("=== Decoded Policy ===")
print(policy)  # This will show the raw policy JSON string

# assemble the 3 Cloudfront cookies
signature = rsa_signer(policy.encode("utf-8"))
encoded_signature = cloudfront_signer._url_b64encode(signature).decode("utf-8")
cookies = {
    "CloudFront-Policy": encoded_policy,
    "CloudFront-Signature": encoded_signature,
    "CloudFront-Key-Pair-Id": key_pair_id,
}
print("cookies[CloudFront-Key-Pair-Id]")
print(cookies["CloudFront-Key-Pair-Id"])
print()
print("cookies[CloudFront-Policy]")
print(cookies["CloudFront-Policy"])
print()
print("cookies[CloudFront-Signature]")
print(cookies["CloudFront-Signature"])
print()

print(
    f"""CloudFront-Key-Pair-Id={cookies["CloudFront-Key-Pair-Id"]};CloudFront-Policy={cookies["CloudFront-Policy"]};CloudFront-Signature={cookies["CloudFront-Signature"]}"""
)
