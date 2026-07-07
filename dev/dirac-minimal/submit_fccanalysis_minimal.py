#!/usr/bin/env python3
"""Submit one FCCAnalyses command through ILCDIRAC.

This is intentionally a minimal proof-of-life script. It is not wired into the
FCCAnalyses CLI and should be edited locally for the first grid tests.
"""

import os
from pathlib import Path

from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import GenericApplication


# Edit these values for the first real test.
ANALYSIS_SCRIPT = "foo.py"
INPUT_LFN = "/fcc/user/b/bwach/2026_06/dev/p8_ee_WW_ecm240_edm4hep.root"
OUTPUT_FILE = "fccanalysis_output.root"
OUTPUT_PATH = "fccanalysis/minimal-test"
OUTPUT_SE = "CERN-DST-EOS"

JOB_NAME = "FCCAnalysis_Minimal"
JOB_GROUP = "FCCAnalysis_Minimal_Run"
SUBMIT_MODE = "wms"  # use "local" for ILCDIRAC local-mode debugging


def normalize_lfn(lfn):
    """ILCDIRAC UserJob.setInputData expects LFNs without an LFN: prefix."""
    if lfn.startswith("LFN:"):
        return lfn[4:]
    return lfn


def lfn_basename(lfn):
    """Return the filename expected after DIRAC stages the input LFN."""
    return os.path.basename(normalize_lfn(lfn))


def require_file(path):
    """Resolve a local file and fail early if it is missing."""
    resolved = Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Required file not found: {resolved}")
    return resolved


def main():
    this_dir = Path(__file__).resolve().parent
    run_script = require_file(this_dir / "run_fccanalysis.sh")
    analysis_path = Path(ANALYSIS_SCRIPT).expanduser()
    if not analysis_path.is_absolute():
        analysis_path = this_dir / analysis_path
    analysis_script = require_file(analysis_path)
    input_lfn = normalize_lfn(INPUT_LFN)
    input_file = lfn_basename(INPUT_LFN)

    d_ilc = DiracILC()

    job = UserJob()
    job.setName(JOB_NAME)
    job.setJobGroup(JOB_GROUP)
    job.setLogLevel("DEBUG")
    job.setOutputSandbox(["*.log", "*.sh", "*.py", "localEnv.log", "std.out", "std.err"])
    job.setInputSandbox([str(analysis_script)])
    job.setInputData(input_lfn)
    job.setOutputData(OUTPUT_FILE, OutputPath=OUTPUT_PATH, OutputSE=OUTPUT_SE)

    app = GenericApplication()
    app.setScript(str(run_script))
    app.setArguments(f"{analysis_script.name} {input_file} {OUTPUT_FILE}")

    job.append(app)

    print("Submitting FCCAnalyses minimal job with:")
    print(f"  analysis script: {analysis_script}")
    print(f"  input LFN:       {input_lfn}")
    print(f"  staged input:    {input_file}")
    print(f"  output file:     {OUTPUT_FILE}")
    print(f"  output path:     {OUTPUT_PATH}")
    print(f"  output SE:       {OUTPUT_SE}")
    print(f"  mode:            {SUBMIT_MODE}")

    print(job.submit(d_ilc, mode=SUBMIT_MODE))


if __name__ == "__main__":
    main()
