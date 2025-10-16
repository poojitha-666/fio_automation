import subprocess
import os
import pytest

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FIO_JOB_FILE = os.path.join(BASE_DIR, "jobs", "storage_validation.fio")
RESULT_DIR = os.path.join(BASE_DIR, "results")

# Ensure results directory exists
os.makedirs(RESULT_DIR, exist_ok=True)

@pytest.mark.parametrize("job_name", [
    "seq-write",
    "seq-read",
    "rand-read",
    "rand-write",
    "randrw-mix"
])
def test_fio_job(job_name):
    """
    Run FIO workload for each job defined in the job file.
    Saves output to a log file.
    """
    log_file = os.path.join(RESULT_DIR, f"{job_name}.log")
    cmd = [
        "fio",
        f"--name={job_name}",
        f"--section={job_name}",
        f"--output={log_file}",
        FIO_JOB_FILE
    ]

    print(f"Running FIO job: {job_name}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Save stdout to log for debugging
    with open(log_file, "a") as f:
        f.write("\n\nSTDOUT:\n")
        f.write(result.stdout)
        f.write("\n\nSTDERR:\n")
        f.write(result.stderr)

    # Assert success
    assert result.returncode == 0, f"FIO job {job_name} failed! Check {log_file}"
