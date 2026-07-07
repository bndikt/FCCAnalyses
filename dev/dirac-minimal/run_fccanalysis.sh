#!/bin/bash
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 ANALYSIS_SCRIPT INPUT_FILE OUTPUT_FILE"
  exit 2
fi

ANALYSIS_SCRIPT="$1"
INPUT_FILE="$2"
OUTPUT_FILE="$3"

KEY4HEP_SETUP="${KEY4HEP_SETUP:-/cvmfs/sw.hsf.org/key4hep/setup.sh}"

echo "Sourcing Key4hep setup: ${KEY4HEP_SETUP}"
source "${KEY4HEP_SETUP}"

echo "Working directory:"
pwd

echo "Directory contents:"
ls -lah

echo "fccanalysis executable:"
which fccanalysis

echo "Running FCCAnalyses:"
fccanalysis run "${ANALYSIS_SCRIPT}" \
  --input "${INPUT_FILE}" \
  --output "${OUTPUT_FILE}"
