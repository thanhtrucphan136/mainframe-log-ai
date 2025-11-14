# app/analyzer.py
import os

# -------------------------------
# Toggle this to switch between mock AI and real GPT
USE_MOCK = True
# -------------------------------

if not USE_MOCK:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")


def explain_job(current_job):
    """
    current_job: dict containing parsed log info
        {
            "jobname": "PAYJOB",
            "cpu_time": 0.02,
            "abend_code": "S0C7",
            "errors": ["IEC130I DD STATEMENT MISSING", "IEF450I ABEND=S0C7"],
            "raw": [ ... full log lines ... ]
        }
    Returns: str - explanation (mock or real GPT)
    """

    if USE_MOCK:
        # Mock explanation for testing without hitting API
        return (
            f"[MOCK AI] \nJob {current_job.get('jobname')} with ABEND={current_job.get('abend_code')} "
            f"\nError(s)\\Warning(s):{len(current_job.get('errors', []))}\n{'\n'.join(current_job.get('errors', []))}"
            "\nPossible causes: ... \nSuggested actions: ..."
        )

    # Real GPT API call
    prompt = f"""
        I have the following mainframe job log details:

        Job Name: {current_job.get('jobname')}
        CPU Time: {current_job.get('cpu_time')}
        ABEND Code: {current_job.get('abend_code')}
        Errors/Warnings:
        {"\n".join(current_job.get('errors', []))}  
        Explain these errors in plain English, suggest possible causes, 
        and recommend steps to fix or investigate. 
        Please follow this format for your response:

        Job <JobName> with ABEND=<ABENDCode>
        Error(s)/Warning(s): <number of errors>
        <list of error/warning(s) messages>
        Possible causes: ...
        Suggested actions: ...
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "You are a helpful mainframe assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        explanation = response.choices[0].message.content.strip()
        return explanation
    except Exception as e:
        return f"Error generating explanation: {e}"
