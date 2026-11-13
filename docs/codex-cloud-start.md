# Start this Codex Cloud environment

Use `/workspace/openai-api-toolkit`, the existing checkout. Each Cloud task is
already isolated. Do not create a Git worktree unless the user explicitly asks.
Read the repository's AGENTS.md before making changes.

The snapshot retains repository files and the installed CLI, not live processes
or personal authentication. This CLI workflow needs no background service.

In Bash:

```bash
cd /workspace/openai-api-toolkit
source scripts/activate.sh
python3 scripts/verify.py
python3 scripts/verify-skill.py
command -v openai
openai --version
```

If the CLI is missing or fails its pinned checksum check, run
`bash scripts/cloud-install.sh`, then activate again in the current shell.
Installation uses Python 3.11+, curl, inherited proxy/CA settings, and the pinned
Linux x86_64 release. It never writes application source or credentials.

The actual Codex Skill loader can need access to its normal configuration path.
If `verify-skill.py` fails because the agent sandbox makes that path read-only,
retry this same check through the platform's approved outside-sandbox execution.
It only initializes the local app-server and calls `skills/list`; it does not
start a model turn. Do not override HOME or CODEX_HOME to bypass the failure.

Read `.agents/skills/openai-cli/SKILL.md` for OpenAI API work. Start a new Codex
session in this checkout if the session's Skill inventory predates installation.
Use focused help, explicit JSON output, ignored result files, and concise summaries.

Before API use, inspect only binding names/readiness and variable presence.
The project uses the standard `OPENAI_API_KEY` environment variable directly.
The wrapper passes the inherited environment unchanged to the official CLI for
authentication. Reuse the existing Personal vault key and restrict its network
destination to `api.openai.com`; never copy its value to files or logs.
Do not rename the user's vault entry or introduce project-specific aliases.
Vault registration does not prove runtime injection. If the platform rejects
`OPENAI_API_KEY` as a reserved target, report that platform limitation explicitly
instead of changing the project's authentication interface.

After environment settings are saved and runtime status confirms the binding
and network policy are applied, run `python3 scripts/check-auth.py` in a fresh
process. Exit 0 means authenticated model listing succeeded; exit 2 means
`OPENAI_API_KEY` is missing (skipped); exit 1 means the check failed. It prints
only a count and saves selected metadata to ignored `results/models.json` on success.
Do not claim authentication passed when skipped or failed. No paid generation
requests are part of setup, startup, or verification.

Keep existing network presets. The explicit required hosts are `api.openai.com`,
`github.com`, `release-assets.githubusercontent.com`, and `raw.githubusercontent.com`.
Saved drafts, runtime application, publication, and validation in a new task are
separate states; check each before claiming it happened.
