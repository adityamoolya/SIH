# backend/test_password.py

from password_utils import verify_password

# --- PASTE THE HASH FROM YOUR DATABASE HERE ---
hashed_password_from_db = "$2b$12$95VeU.lNMaEsdlQm/fQDcusWsH6Q7HFxhBrzgPxevUYRV2wYgVHsK"

# --- TYPE THE PLAIN TEXT PASSWORD YOU USED TO REGISTER ---
password_you_are_typing = "12345"

# --- Run the verification ---
is_match = verify_password(password_you_are_typing, hashed_password_from_db)

print("--- Password Verification Test ---")
print(f"Password matches: {is_match}")
print("--------------------------------")

if is_match:
    print("✅ SUCCESS: The hashing and verification logic is working correctly.")
else:
    print("❌ FAILURE: The passwords do not match. The issue is with the hashing libraries or a typo.")