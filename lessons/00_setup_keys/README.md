# Lesson 0: Set up your API keys (Beginner-friendly)

Goal: get real keys working so later lessons can call actual LLMs and Pinecone without headaches. We'll use free tiers where possible.

## What you'll set up

- LLM provider: Groq (fast, generous free tier) or Hugging Face Inference (free models)
- Vector DB: Pinecone (free tier)
- Local project env: a `.env` file the code reads automatically

If you don't want to use keys yet, you can still explore the viewer with saved graphs, but lessons now require real keys.

## 1) Create a `.env` file

1. Copy the example file:
   - From project root, copy `.env.example` to `.env`.
2. Open `.env` and set these values:
   - GROQ_API_KEY=your_groq_key_here
   - HUGGINGFACE_API_TOKEN=your_hf_token_here (optional)
   - PINECONE_API_KEY=your_pinecone_key_here
   - USE_OPENAI=0 (we'll skip OpenAI for now)

Note: The repo’s `.gitignore` already ignores `.env`.

## 2) Get a Groq API key (LLM)

- Visit https://console.groq.com/keys and create a key
- Paste it into `.env` as GROQ_API_KEY
- Models to try later: `llama3-8b-8192`, `mixtral-8x7b-32768`

## 3) (Optional) Get a Hugging Face token

- Visit https://huggingface.co/settings/tokens
- Create a Read token and paste it into `.env` as HUGGINGFACE_API_TOKEN
- Some hosted models can be called via API with that token

## 4) Set up Pinecone (Vector DB)

- Visit https://app.pinecone.io/ and sign up (free tier)
- Create an API key from the Console
- Paste it into `.env` as PINECONE_API_KEY
- Region: note your project environment (e.g., `us-east-1-aws`)

We won't create indexes yet; Lesson 3 will. For now, we’ll just verify the key.

## 5) Verify your keys with the checker script

From the project root, run the lesson 0 script:

- Python: run `python3 lessons/00_setup_keys/code.py`

It will:
- Load `.env`
- Check GROQ_API_KEY, HUGGINGFACE_API_TOKEN, PINECONE_API_KEY
- Try a tiny test call to Groq (if installed) and Pinecone (REST ping)
- Print clear next steps

If something’s missing, it will tell you exactly what to fix.

## Troubleshooting

- If you see “module not found” for `groq` or `pinecone-client`, install them:
  - They’re listed in `requirements.txt`; ensure your venv is active and run your standard install command.
- If you prefer not to install, the checker will skip runtime tests and only validate presence of keys.

## What’s next

- Lesson 1 uses a real LLM (Groq/OpenAI). With keys set, you’re ready.
- If you also have OpenAI, set `USE_OPENAI=1` and add `OPENAI_API_KEY`.

