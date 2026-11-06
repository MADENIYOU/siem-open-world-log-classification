#!/bin/zsh
# Construit la présentation, applique le thème, ajoute les transitions et valide.  Usage : ./build.sh
cd "$(dirname "$0")"
export PPTX_SKILL_DIR="${PPTX_SKILL_DIR:-/Users/xpertech/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/a6636cf5-77ac-4146-b309-a4cf31869ec1/33216acf-17ff-485f-8b54-a788d7473a54/skills/pptx}"
export NODE_PATH="$PWD/node_modules"
node build_deck.js && .venv/bin/python post_process.py Soutenance_SIEM_monde_ouvert.pptx && .venv/bin/python "$PPTX_SKILL_DIR/scripts/office/validate.py" Soutenance_SIEM_monde_ouvert.pptx
