import os
import base64
import json
import asyncio
from typing import Optional

import aiohttp


class GitHubStorage:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo = os.getenv("GITHUB_REPO")
        self.branch = os.getenv("GITHUB_BRANCH", "main")
        self.file_path = os.getenv(
            "GITHUB_KNOWLEDGE_PATH",
            "data/knowledge.json"
        )

        self.api_url = "https://api.github.com"

    @property
    def enabled(self):
        return bool(self.token and self.repo)

    def _headers(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "Souvion-AI",
        }

    async def load_knowledge(self) -> Optional[dict]:
        """
        Load knowledge.json from GitHub.
        Returns None if GitHub storage is unavailable.
        """

        if not self.enabled:
            return None

        url = (
            f"{self.api_url}/repos/"
            f"{self.repo}/contents/{self.file_path}"
        )

        params = {
            "ref": self.branch
        }

        try:
            async with aiohttp.ClientSession(
                headers=self._headers()
            ) as session:

                async with session.get(
                    url,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:

                    if response.status == 404:
                        print("[GITHUB] knowledge.json not found.")
                        return None

                    if response.status != 200:
                        error_text = await response.text()
                        print(
                            f"[GITHUB] Load failed "
                            f"{response.status}: {error_text}"
                        )
                        return None

                    data = await response.json()

                    encoded_content = data.get("content")

                    if not encoded_content:
                        print("[GITHUB] No file content found.")
                        return None

                    encoded_content = encoded_content.replace("\n", "")

                    decoded = base64.b64decode(
                        encoded_content
                    ).decode("utf-8")

                    knowledge = json.loads(decoded)

                    print("[GITHUB] knowledge.json loaded.")
                    return knowledge

        except asyncio.TimeoutError:
            print("[GITHUB] Load timeout.")
            return None

        except Exception as error:
            print(f"[GITHUB] Load error: {error}")
            return None

    async def save_knowledge(
        self,
        knowledge: dict,
        commit_message: str = "Update Souvion AI knowledge"
    ) -> bool:
        """
        Save knowledge.json to GitHub.
        """

        if not self.enabled:
            print("[GITHUB] Storage is not configured.")
            return False

        url = (
            f"{self.api_url}/repos/"
            f"{self.repo}/contents/{self.file_path}"
        )

        try:
            # Get current file to obtain SHA.
            async with aiohttp.ClientSession(
                headers=self._headers()
            ) as session:

                async with session.get(
                    url,
                    params={"ref": self.branch},
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:

                    current_sha = None

                    if response.status == 200:
                        current_file = await response.json()
                        current_sha = current_file.get("sha")

                    elif response.status != 404:
                        error_text = await response.text()

                        print(
                            f"[GITHUB] Could not read current file "
                            f"{response.status}: {error_text}"
                        )

                        return False

                # Convert JSON to formatted UTF-8 bytes.
                json_text = json.dumps(
                    knowledge,
                    ensure_ascii=False,
                    indent=2
                )

                encoded_content = base64.b64encode(
                    json_text.encode("utf-8")
                ).decode("utf-8")

                payload = {
                    "message": commit_message,
                    "content": encoded_content,
                    "branch": self.branch,
                }

                # SHA is required when updating an existing file.
                if current_sha:
                    payload["sha"] = current_sha

                async with session.put(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:

                    if response.status in (200, 201):
                        result = await response.json()

                        commit = result.get("commit", {})
                        commit_sha = commit.get("sha", "unknown")

                        print(
                            "[GITHUB] Knowledge saved successfully."
                        )
                        print(
                            f"[GITHUB] Commit: {commit_sha}"
                        )

                        return True

                    error_text = await response.text()

                    print(
                        f"[GITHUB] Save failed "
                        f"{response.status}: {error_text}"
                    )

                    return False

        except asyncio.TimeoutError:
            print("[GITHUB] Save timeout.")
            return False

        except Exception as error:
            print(f"[GITHUB] Save error: {error}")
            return False


github_storage = GitHubStorage()
