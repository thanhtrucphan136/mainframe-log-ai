# app/analyzer.py

def explain_job(job):
    abend_dict = {
        "S0C7": "Numeric data exception: usually caused by data type mismatch.",
        "S806": "Program check: check for invalid instructions."
    }

    explanation = f"Job {job['jobname']}:\n"
    if job["abend_code"]:
        code = job["abend_code"]
        explanation += f"- ABEND code: {code}\n"
        explanation += f"- AI explanation (placeholder): {abend_dict.get(code, 'Unknown code, check IBM docs.')}\n"
        explanation += f"- IBM doc: https://www.ibm.com/docs/en/errorcode/{code}\n"
    else:
        explanation += "- Completed successfully\n"

    explanation += f"- CPU time: {job['cpu_time']} sec\n"
    if job["errors"]:
        explanation += f"- Errors/Warnings: {', '.join(job['errors'])}\n"

    return explanation
