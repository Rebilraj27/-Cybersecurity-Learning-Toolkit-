import hashlib
import os

SUPPORTED = ["md5", "sha1", "sha256", "sha512"]

def hash_word(word: str, algo: str) -> str:
    h = hashlib.new(algo)
    h.update(word.encode())
    return h.hexdigest()

def crack(target_hash: str, wordlist_path: str, algo: str = "md5"):
    """Educational dictionary attack demo."""
    if algo not in SUPPORTED:
        raise ValueError(f"Unsupported algo. Use: {SUPPORTED}")
    if not os.path.exists(wordlist_path):
        raise FileNotFoundError(wordlist_path)

    target = target_hash.lower().strip()
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            word = line.strip()
            if not word:
                continue
            if hash_word(word, algo) == target:
                return {"found": True, "password": word,
                        "attempts": i, "algorithm": algo}
    return {"found": False, "attempts": i if 'i' in dir() else 0}
