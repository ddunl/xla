# Copyright 2023 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Provides a Python interface to various parts of the GitHub API."""
import dataclasses
import json
import requests
from typing import Any, Optional

JSON = dict[str, Any]


class GitHubAPI:
  _BASE_URL = "https://api.github.com"
  def __init__(self, token: Optional[str] = None):
    self._session = requests.Session()
    self._session.headers["Accept"] = "application/vnd.github+json"
    if token:
      self._session.headers["Authorization"] = f"token {token}"


  def get_commit_from_hash(self, repo: str, commit_sha: str) -> requests.Response:
    endpoint = f"{self._BASE_URL}/repos/{repo}/commits/{commit_sha}"
    return self._session.get(endpoint)


  def write_issue_comment(self, repo: str, issue_number: int, comment: str) -> requests.Response:
    endpoint = f"{self._BASE_URL}/repos/{repo}/issues/{issue_number}/comments"
    return self._session.post(endpoint, json={"body": comment})


  def set_issue_status(self, repo: str, issue_number: int, status: str) -> requests.Response:
    endpoint = f"{self._BASE_URL}/repos/{repo}/issues/{issue_number}"
    return self._session.get(endpoint)







if __name__ == "__main__":
  import os
  gh_api = GitHubAPI(os.getenv("GH_TOKEN"))
  r = gh_api.get_commit_from_hash("openxla/xla", "c560e8")
  print(r.json())
  r = gh_api.write_issue_comment("ddunl/xla", 2, "hello from github API!")
  print(r.json())









