# Minimal FCCAnalyses ILCDIRAC Test

This directory is a proof-of-life test for running one FCCAnalyses job through
ILCDIRAC/DIRAC. It intentionally does not integrate with `fccanalysis submit`.

Goal:

```text
one analysis script + one input LFN -> one DIRAC job -> one output ROOT file
```

## Files

- `submit_fccanalysis_minimal.py`: user-side ILCDIRAC submission script
- `run_fccanalysis.sh`: worker-side script run through `GenericApplication`

## How To Use

Edit the configuration block at the top of `submit_fccanalysis_minimal.py`:

```python
ANALYSIS_SCRIPT = "path/to/foo.py"
INPUT_LFN = "/path/to/input.root"
OUTPUT_FILE = "fccanalysis_output.root"
OUTPUT_PATH = "fccanalysis/minimal-test"
OUTPUT_SE = "CERN-DST-EOS"
```

Then run from an ILCDIRAC client environment:

```bash
source /cvmfs/clicdp.cern.ch/DIRAC/bashrc
dirac-proxy-init -g fcc_user
python dev/dirac-minimal/submit_fccanalysis_minimal.py
```

To test the ILCDIRAC workflow locally before sending it to the WMS, change:

```python
SUBMIT_MODE = "local"
```

or leave it as:

```python
SUBMIT_MODE = "wms"
```

for real grid submission.

## Expected Worker Command

The worker script runs:

```bash
source /cvmfs/sw.hsf.org/key4hep/setup.sh
fccanalysis run <analysis.py> --input <staged-input-basename> --output <output.root>
```

The staged input name is assumed to be the basename of the input LFN. The script
prints `pwd`, `ls -lah`, and `which fccanalysis` before running, so the first
logs should make input staging and environment failures clear.
