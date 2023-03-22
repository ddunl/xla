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
import itertools
import json
import logging
import os
import re
import subprocess
import sys
from typing import Generator, Optional, Sequence



def call_gh_api(endpoint: str, *, http_method: str = "GET", **kwargs):
  # Just want to flatten the list.... why is it so ugly
  fields = itertools.chain(*[("-f", f"{k}='{v}'") for k, v in kwargs.items()])

  subprocess.run(
      ["gh", "api", "--method", http_method, endpoint, *fields],
        capture_output=True,
        check=True,
        text=True,
  )

  return json.loads(proc.stdout)


def get_reverted_shas(message: str) -> list[str]:
  regex = re.compile("[Rr]everts ([0-9a-f]{5,40})")
  shas = regex.findall(message)
  logging.info("Found shas reverted in this commit: %s", shas)
  return shas


def get_associated_prs(shas: Sequence[str]) -> Generator[tuple[str, int], None, None]:
  # Necesary because of copybara
  for sha in shas:
    regex = re.compile("PR #(\\d+)")
    response = call_gh_api(f"repos/ddunl/xla/commits/{sha}")
    message = response["commit"]["message"]
    if maybe_match := re.match(message):
      pr_number = int(maybe_match.group())
      logging.info("Found PR #%s associated with sha %", pr_number, sha)
      yield sha, pr_number


def write_pr_comment_and_reopen(sha: str, pr_number: int) -> None:
  comment_body = f"This PR was rolled back in {sha}!"
  
  # write PR comment
  call_gh_api(f"/repos/ddunl/xla/issues/{pr_number}/comments",
      http_method="POST", body=comment_body)

  # reopen PR
  call_gh_api(f"/repos/ddunl/xla/issues/{pr_number}", http_method="POST", state="open")


def main():
  head_commit_message = os.getenv("HEAD_COMMIT_MESSAGE")
  if head_commit_message is None:
    raise EnvironmentError("Environment variable HEAD_COMMIT_MESSAGE not set!")

  shas = get_reverted_shas(head_commit_message)

  
  for sha, pr_number in get_associated_prs(shas):
    write_pr_comment_and_reopen(sha, pr_number)


if __name__ == "__main__":
    main()
