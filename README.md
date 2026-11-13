# OpenAI API Toolkit

공식 [OpenAI CLI](https://github.com/openai/openai-cli)와 공식 CLI Skill을 사용하는
재사용 가능한 Codex Cloud 및 Linux 로컬 작업 환경입니다. CLI는 OpenAI REST API 도구이며,
코딩 에이전트인 Codex CLI와는 별도 프로그램입니다.

## 고정한 버전과 출처

| 구성요소 | 버전 / 출처 |
| --- | --- |
| OpenAI CLI | 공식 안정 릴리스 [v1.53.1](https://github.com/openai/openai-cli/releases/tag/v1.53.1) |
| 설치 지원 플랫폼 | Linux x86_64 (`linux_amd64`), 동일 아키텍처의 WSL2 및 Codex Cloud |
| 공식 Skill | 같은 릴리스의 `skills/openai-cli/`, 원본 내용 그대로 포함 |
| 소스 커밋 | `fb2a8bf24693e391b0a6bac2bb6c004fa15085cb` |
| 무결성 기록 | [config/openai-cli.lock.json](config/openai-cli.lock.json) |
| Skill 출처·라이선스 | [.agents/skills/openai-cli/SOURCE.md](.agents/skills/openai-cli/SOURCE.md), Apache-2.0 |

설치기는 공식 릴리스의 SHA-256 목록에서 고정한 아카이브 해시와 바이너리 해시를
검증합니다. 자동 업데이트와 업데이트 조회를 비활성화해 재실행해도 같은 버전을
사용합니다. 버전 변경 시에는 공식 릴리스와 체크섬을 다시 확인하고 CLI·Skill·문서의
버전 기록을 함께 갱신해야 합니다.

## 로컬에서 가져오기

Linux x86_64 또는 같은 아키텍처의 WSL2에서 Bash, Python 3.11 이상, curl, Git을
준비한 뒤 실행합니다. 현재 설치 스크립트는 macOS와 Windows 네이티브를 지원하지 않습니다.

```bash
git clone https://github.com/twoeater/openai-api-toolkit.git
cd openai-api-toolkit
bash scripts/cloud-install.sh
source scripts/activate.sh
openai --version
```

`cloud-install.sh`라는 이름이지만 설치 경로는 현재 체크아웃을 기준으로 계산하므로
로컬에서도 같은 절차를 사용합니다. 공식 바이너리 다운로드와 오프라인 검증에는 키가
필요하지 않습니다. 이후 변경을 가져오려면 다음 명령을 실행합니다.

```bash
git pull --ff-only
bash scripts/cloud-install.sh
source scripts/activate.sh
```

API 인증은 로컬의 보안 시크릿 관리 도구가 `OPENAI_API_KEY`를 제공한 셸에서
`python3 scripts/check-auth.py`로 확인합니다. Cloud의 Personal vault 연결이나 프록시
자리표시자는 Git에 포함되지 않으며 로컬로 복사하지 않습니다.

Skill을 사용하려면 로컬에도 Codex가 설치되어 있어야 합니다. 이 체크아웃에서 새 Codex
세션을 시작하면 `.agents/skills/openai-cli/`를 프로젝트 Skill로 인식합니다. 다른
프로젝트에서는 CLI 활성화 경로를 이 체크아웃으로 지정하고, Skill도 해당 프로젝트에
설치해야 합니다.

## Codex Cloud에서 설치와 새 작업 시작

필요 도구는 Bash, Python 3.11 이상, curl, Git입니다. 기본 Codex Cloud 이미지에서
제공하며, 시스템 패키지 설치나 관리자 권한은 필요하지 않습니다.

```bash
cd /workspace/openai-api-toolkit
bash scripts/cloud-install.sh
source scripts/activate.sh
command -v openai
openai --version
openai --help
```

바이너리는 Git에서 제외한 `.local/openai-cli/1.53.1/openai`에 설치됩니다.
`bin/openai`가 이 공식 바이너리를 실행합니다. 인증은 공식 CLI의 표준 환경변수
`OPENAI_API_KEY`를 그대로 사용하며, 래퍼가 값을 변경하거나 다른 이름으로 변환하지 않습니다.
다른 위치에 체크아웃했다면 해당 디렉터리에서 같은 명령을 실행하면 됩니다.
재설치는 이미 설치된 바이너리의 체크섬을 확인하며, Skill 파일을 덮어쓰지 않습니다.

새 셸에서는 `source scripts/activate.sh`를 다시 실행합니다. 새 Cloud 작업에서도
기존 체크아웃을 사용하며, 별도 Git worktree나 백그라운드 서버가 필요하지 않습니다.
환경의 설치 스크립트에는 다음 절차를 저장합니다.

```bash
set -euo pipefail
cd /workspace/openai-api-toolkit
bash scripts/cloud-install.sh
```

시작 지침 전체는 [docs/codex-cloud-start.md](docs/codex-cloud-start.md)에 있습니다.
환경 설정의 초안 저장은 스크립트 실행이나 게시와 별개입니다. 설정을 검토·저장한 뒤
**Publish**해야 준비한 파일과 설정을 이후 작업에서 재사용할 수 있습니다.
Git만으로 새로 체크아웃하는 경우에는 이 저장소의 설정 파일들이 원격에 커밋되어
있어야 합니다. 게시된 Cloud 스냅샷은 준비된 파일시스템을 사용합니다.

## 개인 API 키 등록

키 원문은 채팅에 보내거나 `.env`, 설정 파일, 로그, 셸 프로필에 넣지 않습니다.

1. **Personal vault**에 저장한 `OPENAI_API_KEY`를 재사용합니다. 이미 등록된 키의
   이름을 바꾸거나 값을 다시 입력하지 않습니다. 처음 등록할 때만 플랫폼의 보안 UI를 사용합니다.
2. Codex Cloud **환경 설정 → Network secrets**의 개인용 연결을 확인합니다.
   프로젝트가 요구하는 프로세스 환경변수 이름은 `OPENAI_API_KEY`이며, 키의 허용 목적지는
   `api.openai.com`입니다. 로컬 실행이나 다른 CI에서도 같은 환경변수 이름을 사용합니다.
3. 보관함 등록과 실제 프로세스 주입은 별개입니다. 플랫폼에서 해당 이름의 주입을
   제한한다면 플랫폼 제약을 해결해야 하며, 프로젝트에 전용 별칭을 추가하지 않습니다.
4. 런타임에서 연결 상태와 변수의 존재 여부만 확인한 뒤 새 프로세스에서 인증을 검증합니다.

```bash
python3 scripts/check-auth.py
```

Cloud에는 프록시가 사용하는 자리표시자가 주입될 수 있습니다. CLI는 제공된
`OPENAI_API_KEY`를 그대로 사용하고, 플랫폼 프록시가 허용된 HTTPS 목적지에서 인증을
처리합니다. 실제 키를 꺼내거나 값이 보이지 않는다는 이유로 다시 등록하지 않습니다.
환경변수 값을 출력하거나 `set -x`, HTTP 디버그 로깅을 켜지 않습니다.

인증 검사는 `openai models list --format json`만 실행합니다. 성공하면 모델 수만 출력하고
선택한 메타데이터를 Git에서 제외된 `results/models.json`에 저장합니다. 오류 원문은 키
일부를 포함할 수 있어 출력·저장하지 않습니다. 종료 코드 0은 성공, 2는 `OPENAI_API_KEY` 미주입으로
건너뜀, 1은 실패입니다. 생성·업로드·배치 제출 요청은 초기화에서 실행하지 않습니다.

## 네트워크 허용 범위

기존 패키지 관리자 프리셋을 보존하고 다음 호스트만 명시적으로 추가합니다.

| 호스트 | 용도 |
| --- | --- |
| `api.openai.com` | API 요청과 개인 키의 유일한 전송 목적지 |
| `github.com` | 공식 릴리스와 Git 소스 |
| `release-assets.githubusercontent.com` | GitHub 릴리스 다운로드 리디렉션 |
| `raw.githubusercontent.com` | 고정 커밋의 공식 Skill·문서 원본 |

설치에는 API 키가 필요하지 않습니다. 상속된 HTTPS 프록시와 CA 인증서를 사용하며,
TLS 검사나 체크섬 검증을 끄지 않습니다.

## CLI와 Skill 사용

공식 Skill은 [.agents/skills/openai-cli/SKILL.md](.agents/skills/openai-cli/SKILL.md)에
있습니다. 공식 문서의 수동 설치 방식대로 전체 Skill 폴더를 복사했습니다.
이 릴리스의 폴더에는 `SKILL.md` 하나가 있으며, 출처 문서와 원본 라이선스를 추가했습니다.

설치 뒤 이 저장소에서 새 Codex 세션을 시작하면 프로젝트 Skill로 탐색됩니다.
예를 들어 `$openai-cli`를 지정하고 “사용 가능한 모델을 조회하고 개수만 요약해줘”라고
요청할 수 있습니다. CLI의 `skills` 명령은 API에 저장된 원격 Skill 번들용이므로,
로컬 Codex Skill 인식 검사에 사용하지 않습니다.

```bash
source scripts/activate.sh
openai --version
openai explore models
openai models list --help
python3 scripts/check-auth.py
```

기타 작업에서는 해당 명령의 도움말만 확인하고, JSON 결과는 `results/`나 `outputs/`에
저장한 뒤 종료 상태를 확인하고 요약과 경로만 반환합니다. 전체 운영 원칙은
[AGENTS.md](AGENTS.md)에 있습니다.

## 검증과 공개 저장소 관리

```bash
python3 scripts/verify.py
python3 scripts/verify-skill.py
python3 scripts/check-auth.py
git status --short --untracked-files=all
```

오프라인 검증은 바이너리·Skill·라이선스의 고정 해시, CLI 버전 및 도움말,
인증정보·실행 결과의 Git 제외 규칙을 확인합니다. 인증 검사는 별도 결과로 판정합니다.
새 작업의 Skill 목록에는 `openai-cli`가 프로젝트 범위로 보여야 합니다.
`verify-skill.py`는 Codex의 실제 `skills/list` 로더를 호출합니다. 모델 대화를 시작하지
않고, 쓰기 가능한 임시 상태 경로를 사용한 뒤 해당 프로세스와 상태를 정리합니다.
Cloud 에이전트 샌드박스에서 Codex 설정 경로가 읽기 전용이면 이 검사만 플랫폼의
승인된 샌드박스 외부 실행으로 재시도합니다. `HOME`이나 `CODEX_HOME`을 바꾸지 않습니다.

`.gitignore`는 `.env` 계열, 인증 파일, 개인 키, 로그, 다운로드한 바이너리와 개인 실행
결과를 제외합니다. 개인 입력 파일도 `private/`에 보관합니다. 이미 추적 중인 파일은
`.gitignore`로 숨겨지지 않으므로 커밋 전 변경 목록을 확인합니다. CLI 바이너리·키·로그·
개인 결과를 커밋하지 않고 문서, 설치 스크립트, 고정 버전 정보와 공식 Skill만 관리합니다.
