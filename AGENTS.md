# Working in this repository

- Work in the existing checkout: `/workspace/openai-api-toolkit` in Codex Cloud,
  or the user's clone directory locally. Each Cloud task is already isolated;
  do not create a Git worktree unless the user asks.
- Run `source scripts/activate.sh` in Bash before using `openai`. The repository
  wrapper selects the locked official `openai/openai-cli` release. Authentication
  uses the standard `OPENAI_API_KEY` environment variable directly, without
  renaming or overriding it. Keep this interface portable across environments.
- Prefer the official OpenAI CLI for supported OpenAI API operations. Read
  `.agents/skills/openai-cli/SKILL.md` and check `openai --version` first; a Python
  SDK can expose a different executable with the same name.
- Read only the help relevant to the task, such as `openai models list --help`.
  Use `openai explore <keywords>` for offline discovery. Do not dump the full
  command reference or all subcommand help into the conversation.
- Request `--format json` or `--format jsonl` when processing API data. Save
  large outputs under ignored `results/` or `outputs/`, check the exit status,
  and return a short summary and the file path. Treat failed output as incomplete.
- Use Personal vault / Network secret UI for keys. Never ask for raw keys in
  chat, print environment values, enable shell tracing around credentials, or
  save keys in `.env`, config, logs, shell profiles, or the repository. Do not
  alter inherited proxies or disable TLS/checksum verification.
- Reuse an existing Personal vault key. Do not rename the user's vault entry or
  add project-specific credential aliases. If a platform cannot provide
  `OPENAI_API_KEY`, report that platform limitation separately from the code.
- API errors and debug output can contain credentials or private content.
  Use `python3 scripts/check-auth.py` for authentication checks; it suppresses
  raw errors. Do not enable `--debug`, `--debug-body`, or log HTTP headers for setup.
- Initialization and verification must not run paid generation, uploads, or
  batch submissions. Authentication verification is limited to `models list`.
  Other remote operations require a corresponding user request.
- Keep the official vendored Skill unchanged. Its source, version, license,
  and checksums are recorded in `config/openai-cli.lock.json` and its `SOURCE.md`.
  Do not use `latest` or enable auto-updates in reusable setup instructions.
- After setup changes, run `bash scripts/cloud-install.sh`. This installs or
  verifies the pinned CLI and runs offline checks. Use the authentication check
  only after the personal binding and `api.openai.com` policy are applied.
