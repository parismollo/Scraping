from collections import Counter

def get_domain(email_address: str) -> str:
    return email_address.lower().split("@")[-1]

assert get_domain("parismollo@email.com") == "email.com"
assert get_domain("claire@other_email.com") == "other_email.com"

with open("email_addresses.txt", "r") as f:
    domain_counts = Counter(get_domain(line.strip()) for line in f if "@" in line)
    print(domain_counts)
