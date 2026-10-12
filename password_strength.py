import re
import math
import string

def entropy(password: str) -> float:
    """Estimate password entropy in bits."""
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"\d", password): pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): pool += 32
    if pool == 0:
        return 0.0
    return len(password) * math.log2(pool)

def analyze(password: str) -> dict:
    score = 0
    feedback = []

    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    else: feedback.append("Use at least 12 characters")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Mix upper and lowercase")

    if re.search(r"\d", password): score += 1
    else: feedback.append("Add numbers")

    if re.search(r"[^A-Za-z0-9]", password): score += 1
    else: feedback.append("Add symbols")

    common = ["password", "123456", "qwerty", "admin", "letmein"]
    if any(c in password.lower() for c in common):
        score = 0
        feedback.append("Contains common weak pattern")

    ent = entropy(password)
    strength = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"][min(score, 5)]

    return {"score": score, "strength": strength,
            "entropy_bits": round(ent, 1), "feedback": feedback}
