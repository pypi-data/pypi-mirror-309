import base64

encoded_policy = "eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly8qLnN0aXRjaC5mYXNoaW9uLyotc3RhZ2luZy8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzMyMTEyMzI2fX19XX0_"


print("\n=== Decoded Policy ===")
try:
    decoded_policy = base64.b64decode(
        encoded_policy.replace("-", "+").replace("_", "/")
    ).decode("utf-8")
    print(decoded_policy)
except UnicodeDecodeError as e:
    print("Raw decoded bytes:")
    raw_bytes = base64.b64decode(encoded_policy.replace("-", "+").replace("_", "/"))
    print(raw_bytes)
    # Try to decode with different encodings or print hex
    print("\nHex representation:")
    print(raw_bytes.hex())

print()
