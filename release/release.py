#!/usr/bin/env python

import argparse
import os
import re
import sys
import yubico

from github import Github


def get_valid_input(msg, pattern):
  p = re.compile(pattern)
  while True:
    result = raw_input(msg + ": ")
    if p.match(result):
      return result


def main():
  #TODO: try to get this to work to avoid needing the separate API token?
  #print "Getting yubikey token..."
  #yk = yubico.find_yubikey(debug=True)
  #print yk

  # Parse all arguments
  parser = argparse.ArgumentParser(description="Release the agent.")
  parser.add_argument("api_token_file", help="File containing a single line: your github API token.")
  parser.add_argument("repo_name", help="Name of the github repo to release into.")
  parser.add_argument("commit_id", help="Commit ID of this release.")
  parser.add_argument("asset_dir", help="Directory containing assets to upload (binaries, etc.)")
  args = parser.parse_args()

  # Validate input
  if not os.path.isfile(args.api_token_file):
    parser.print_help()
    raise SystemExit("%s does not exist or is not a file." % args.api_token_file)

  if not os.path.isdir(args.asset_dir):
    parser.print_help()
    raise SystemExit("%s does not exist or is not a directory." % args.asset_dir)

  if not re.match("^[0-9a-f]{40}$", args.commit_id):
    parser.print_help()
    raise SystemExit("%s is not a valid commit_id." % args.commit_id)

  # Read our GitHub API token from the designated file.
  api_token = ''
  with open(args.api_token_file) as f:
    api_token = f.readline().strip()

  # Initialize GitHub client and look up our repo.
  gh = Github(api_token)
  repo = gh.get_repo(args.repo_name)

  print "Checking existing releases..."
  for release in repo.get_releases():
    if release.draft:
      print "ERROR: Release '{0}' is already a draft; Publish that release first, or discard it and make a new one.".format(release.title)
      sys.exit(1)

  release_name = get_valid_input("Enter release name", ".{10}")
  release_tag = get_valid_input("Enter a release tag (must be of format 'v1.0.0')", "^v\d+\.\d+\.\d+$")

  print "Creating new draft release..."
  release = repo.create_git_tag_and_release(
      tag=release_tag,
      tag_message="tag message for " + release_tag,
      release_name=release_name,
      release_message="Release: %s\nbased on commit: %s" % (release_name, args.commit_id),
      object=args.commit_id,
      type="commit",
      draft=True,
      prerelease=True)

  print "Uploading assets..."
  for (dirpath, dirnames, filenames) in os.walk(args.asset_dir):
    for filename in filenames:
      print "  Uploading " + filename + "..."
      release.upload_asset(os.path.join(args.asset_dir, filename))

if __name__ == "__main__":
  main()
