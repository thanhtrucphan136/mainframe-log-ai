import re

JOB_START_PATTERN = re.compile(r'^\$HASP\d+\s+(\S+)')
CPU_PATTERN = re.compile(r'CPU TIME=(\d+\.\d+)')
ABEND_PATTERN = re.compile(r'ABEND=(\S+)')
ERROR_PATTERN = re.compile(r'^(IEC|IEF)\d+.*')

def parse_log(file_path):
    logs = []
    current_job = None

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()

            job_start = JOB_START_PATTERN.match(line)
            if job_start:
                if current_job:
                    logs.append(current_job)
                current_job = {"raw": [], "jobname": job_start.group(1), "cpu_time": 0, "abend_code": None, "errors": []}

            if not current_job:
                continue

            current_job["raw"].append(line)

            cpu_match = CPU_PATTERN.search(line)
            if cpu_match:
                current_job["cpu_time"] = float(cpu_match.group(1))

            abend_match = ABEND_PATTERN.search(line)
            if abend_match:
                current_job["abend_code"] = abend_match.group(1)

            error_match = ERROR_PATTERN.match(line)
            if error_match:
                current_job["errors"].append(line)

    if current_job:
        logs.append(current_job)
    return logs
