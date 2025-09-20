"""
Lesson 0: Key checker
- Loads .env
- Verifies presence of beginner-friendly keys (Groq, Hugging Face, Pinecone)
- Optionally runs tiny test calls if clients are installed
- Prints actionable guidance without failing the run
"""
import os
import sys
import json
from typing import Tuple

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

def status(ok: bool) -> str:
    return "✅" if ok else "❌"


def check_env_var(name: str) -> Tuple[bool, str]:
    val = os.getenv(name)
    if val and not val.startswith("get_from_") and val.strip() != "":
        return True, "present"
    return False, "missing"


def try_groq() -> Tuple[bool, str]:
    key_ok, _ = check_env_var("GROQ_API_KEY")
    if not key_ok:
        return False, "GROQ_API_KEY not set"
    try:
        from groq import Groq
    except Exception:
        return False, "groq package not installed (optional)"
    try:
        client = Groq(api_key=os.environ["GROQ_API_KEY"]) 
        # Minimal ping-like call
        client.models.list()
        return True, "Groq client working (models.list)"
    except Exception as e:
        return False, f"Groq error: {e}"


def try_pinecone() -> Tuple[bool, str]:
    key_ok, _ = check_env_var("PINECONE_API_KEY")
    if not key_ok:
        return False, "PINECONE_API_KEY not set"
    # Prefer not to force-install pinecone-client; do a lightweight REST check
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(
            url="https://api.pinecone.io/actions/whoami",
            headers={
                "Api-Key": os.environ["PINECONE_API_KEY"],
                "Content-Type": "application/json",
            },
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                project = data.get("projectId") or data.get("project_name") or "unknown"
                return True, f"Pinecone key valid (project: {project})"
            return False, f"Pinecone HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"Pinecone HTTPError: {e.code}"
    except Exception as e:
        return False, f"Pinecone error: {e}"


def main():
    if load_dotenv:
        load_dotenv()
    print("\n🔐 Lesson 0: Key checker")
    print("========================\n")

    checks = {
        "GROQ_API_KEY": check_env_var("GROQ_API_KEY"),
        "HUGGINGFACE_API_TOKEN": check_env_var("HUGGINGFACE_API_TOKEN"),
        "PINECONE_API_KEY": check_env_var("PINECONE_API_KEY"),
    }

    for name, (ok, msg) in checks.items():
        print(f"{status(ok)} {name}: {msg}")

    # Optional runtime tests
    groq_ok, groq_msg = try_groq()
    print(f"{status(groq_ok)} Groq test: {groq_msg}")

    pine_ok, pine_msg = try_pinecone()
    print(f"{status(pine_ok)} Pinecone test: {pine_msg}")

    print("\nNext steps:")
    if not checks["GROQ_API_KEY"][0]:
        print("- Get a Groq key at https://console.groq.com/keys and set GROQ_API_KEY in .env")
    if not checks["PINECONE_API_KEY"][0]:
        print("- Get a Pinecone key at https://app.pinecone.io/ and set PINECONE_API_KEY in .env")
    if not checks["HUGGINGFACE_API_TOKEN"][0]:
        print("- (Optional) Create a token at https://huggingface.co/settings/tokens and set HUGGINGFACE_API_TOKEN in .env")

    print("\nTip: With keys set, you can run Lesson 1 using Groq (default) or OpenAI.")

if __name__ == "__main__":
    main()
