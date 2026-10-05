{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Bash(git push --force:*)",
      "Bash(git push -f:*)",
      "Bash(rm -rf /:*)",
      "Bash(rm -rf ~:*)"
    ]
  }
}
