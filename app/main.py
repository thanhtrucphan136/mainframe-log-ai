from .parser import parse_log
from .analyzer import explain_job

if __name__ == "__main__":
    log_file = "data/syslog.txt"
    parsed_logs = parse_log(log_file)

    for job in parsed_logs:
        output = explain_job(job)
        print(output)
        print("-" * 50)
