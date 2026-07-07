# FCCAnalyses Grid Submission Plan

## Goal

Add support for submitting FCCAnalyses jobs to the DIRAC managed grid, using
the ILCDIRAC/DIRAC client environment available to the user.

The first design pass should stay high level. Detailed command-line options,
exact file formats, and implementation choices can be filled in after the
existing HTCondor submission path is understood.

## Current Entry Point

The existing user-facing entry point should remain:

```bash
fccanalysis submit <analysis.py>
```

The submit command should decide which backend is being used, then delegate to
backend-specific code. The top-level submission code should stay thin.

Conceptually:

```text
analysis script
  -> FCCAnalyses submission frontend
  -> backend-specific submission implementation
```

## Starting Grid Model

For the first grid design iteration, use a simple mapping:

```text
one input file -> one DIRAC job
```

This is intentionally simpler than the current HTCondor chunking model. It
should make it easier to reason about generated DIRAC jobs and debug early
grid submissions.

Questions to revisit later:

- Should grid submission eventually reuse the HTCondor chunking logic?
- Should FCCAnalyses introduce a backend-neutral job planning layer?
- Should one DIRAC job ever process multiple input files?
- How should user-requested `chunks` interact with one-file-per-job grid mode?

## High-Level Responsibilities

### Analysis Loading

Reuse the existing dynamic import approach from `submit.py`.

The analysis script remains the source of truth for:

- which samples/processes to run
- where inputs come from
- which analysis code should execute
- how output files are named at the FCCAnalyses level

### Grid Job Description

The grid backend should translate FCCAnalyses work into DIRAC/ILCDIRAC job
descriptions or ready-to-submit Python scripts.

At first, generating ready-to-submit artifacts is preferable to immediately
submitting them. This gives users a chance to inspect what FCCAnalyses would
send to DIRAC.

### Worker Execution

Each remote job should run a familiar FCCAnalyses command on the worker node.

Conceptually:

```bash
fccanalysis run <analysis.py> --input <one input file> --output <output.root>
```

The worker wrapper is responsible for setting up the required runtime
environment before running that command.

### Input Data

The grid design should treat input files as DIRAC-managed data, not arbitrary
local files.

Initial assumption:

```text
input file paths should be DIRAC LFNs or values that can be unambiguously
converted to DIRAC LFNs
```

This assumption should be checked against real FCCAnalyses sample metadata and
ILCDIRAC expectations before implementation.

### Output Data

Output handling is a major architecture decision and should be discussed before
implementation.

Likely direction:

- stdout/stderr/logs go to the DIRAC output sandbox
- ROOT output files are registered as DIRAC output data

Details such as storage element, output path, naming, and metadata should be
specified later.

## Open Architecture Questions

- Should the grid backend live in a new module, or should submission code first
  be reorganized around a shared job-planning layer?
- Should HTCondor and DIRAC share a common representation of planned work?
- What minimum DIRAC/ILCDIRAC environment checks should FCCAnalyses perform?
- How should failures be reported when a generated DIRAC job script is invalid
  or submission fails?
- What should be documented as user setup versus handled by FCCAnalyses?

## Current Preference

Start with a conservative, inspectable workflow:

```text
FCCAnalyses analysis script
  -> one planned grid job per input file
  -> generated DIRAC/ILCDIRAC submission artifact
  -> user manually submits or tests the generated artifact
```

Once generated artifacts are known to be correct, automatic submission can be
added as a second step.
