#!/usr/bin/env python

import os
import sys
import yubico

from github import Github

# Populated by parent script.
# (TODO: don't be lazy, make these command line arguments or something...)
API_TOKEN_FILE = os.environ.get("API_TOKEN_FILE")
SNAPSHOT_COMMIT = os.environ.get("SNAPSHOT_COMMIT")
SNAPSHOT_BRANCH = os.environ.get("SNAPSHOT_BRANCH")
ASSET_DIR = os.environ.get("ASSET_DIR")

REPO_NAME = "tzsebe/release-experimentation"

def main():
  #TODO: try to get this to work to avoid needing the separate API token?
  #print "Getting yubikey token..."
  #yk = yubico.find_yubikey(debug=True)
  #print yk

  print "Reading token..."
  api_token = ''
  with open(API_TOKEN_FILE) as f:
    api_token = f.readline().strip()

  print "Token (head) is: ", api_token[:3]

  print "Initializing github object..."
  gh = Github(api_token)

  #for repo in gh.get_user().get_repos():
  #  print repo.full_name

  repo = gh.get_repo(REPO_NAME)

  print "Checking existing releases..."
  for release in repo.get_releases():
    print "{0}\t{1}".format(release.tag_name, release.title)
    if release.draft:
      print "Release {0} is already a draft; Publish that release first, or discard it and make a new one.".format(release.title)
      sys.exit(1)


  release_name = raw_input("Enter release name: ")
  release_tag = raw_input("Enter git tag for release: ")

  print "Creating new draft release..."
  release = repo.create_git_tag_and_release(
      tag=release_tag,
      tag_message="tag message for " + release_tag,
      release_name=release_name,
      release_message="release message for " + release_name,
      object=SNAPSHOT_COMMIT,
      type="commit",
      draft=True,
      prerelease=True)

  print "Uploading assets..."
  for (dirpath, dirnames, filenames) in os.walk(ASSET_DIR):
    for filename in filenames:
      print "  Uploading " + filename + "..."
      release.upload_asset(os.path.join(ASSET_DIR, filename))

if __name__ == "__main__":
  main()
