def decode_domain_name(encoded_domain_name: str) -> str:
  return bytes.fromhex(encoded_domain_name).decode("utf-8").replace("\u0000", "")

def encode_domain_name(domain_name: str) -> str:
  if domain_name.includes(".") or "\u0000" in domain or '"' in domain:
    raise Exception("Domain name cannot include '.' or '\"' or '\\u0000'");
  hex_encoded = domain_name.encode("utf-8").hex()
  if len(hex_encoded) > 64:
    raise Exception("Cannot be more than 32 bytes")
  if len(hex_encoded) < 64:
    hex_encoded = "0" * (64 - len(hex_encoded)) + hex_encoded
  return hex_encoded

