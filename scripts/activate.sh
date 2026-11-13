# Source from Bash: source scripts/activate.sh
OPENAI_TOOLKIT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
export OPENAI_TOOLKIT_ROOT
case ":$PATH:" in
  *":$OPENAI_TOOLKIT_ROOT/bin:"*) ;;
  *) export PATH="$OPENAI_TOOLKIT_ROOT/bin:$PATH" ;;
esac
