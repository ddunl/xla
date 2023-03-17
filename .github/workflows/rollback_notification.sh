#!/bin/bash
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
SHA=$(echo $HEAD_COMMIT_MESSAGE | jq --raw-input --raw-output 'match("Reverts ([0-9a-f]{40})").captures[0].string')

if [ $SHA ]; then
  PR=$(gh api repos/openxla/xla/commits/$SHA | jq --raw-output '.commit.message | match("^PR #(\\d+)").captures[0].string')
  if [ $PR ]; then
    echo "Commenting on PR ${PR}..."
    gh api \
      --method POST \
      -H "Accept: application/vnd.github+json" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      /repos/openxla/xla/issues/$PR/comments \
      -f body='This PR was rolled back in ${GITHUB_SHA}!'
  else
    echo "This commit seems to be a rollback, but the commit being rolled back isn't associated with a PR."
  fi
else
  echo "This commit doesn't appear to be a rollback."
fi


