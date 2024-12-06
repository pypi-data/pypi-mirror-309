import os
import requests

# Retrieve GitHub Personal Access Token from environment variable
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    print("Error: GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
    exit(1)

# List of repositories to delete (format: "owner/repo")
REPOS = [
    "jakerains/ai-photo-booth",
    "jakerains/amplify-next-template",
    "jakerains/assistantapi",
    "jakerains/autotrain_dreambooth",
    "jakerains/bolt.new-any-llm",
    "jakerains/chatgpt-artifacts",
    "jakerains/chattest1",
    "jakerains/diffusionbooth",
    "jakerains/exo",
    "jakerains/Fooocus",
    "jakerains/JetsonInnovationDemo",
    "jakerains/LLaMA-Factory",
    "jakerains/llamanet",
    "jakerains/nextjs-ai-chatbot",
    "jakerains/oaiassist",
    "jakerains/ollama",
    "jakerains/Ollama-Colab-Integration",
    "jakerains/open-webui",
    "jakerains/openai-realtime-console",
    "jakerains/openaiassistant",
    "jakerains/PhotoMaker",
    "jakerains/pluto",
    "jakerains/Rivertown-aws",
    "jakerains/Rivertownballaws"
]

# API headers for authentication
HEADERS = {"Authorization": f"token {TOKEN}"}

# Function to delete repositories
def delete_repo(repo):
    url = f"https://api.github.com/repos/{repo}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Deleted: {repo}")
    else:
        print(f"Failed to delete {repo}: {response.status_code} - {response.text}")

# Iterate through and delete repositories
for repo in REPOS:
    delete_repo(repo)
