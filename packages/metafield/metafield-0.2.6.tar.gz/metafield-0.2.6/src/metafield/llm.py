from litellm import completion
from .git_utils import get_commit_message

def remindme(*, since="7 days ago", repo_dir=None):
  if not repo_dir:
    import subprocess
    repo_dir = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
    repo_dir = repo_dir.decode("utf-8").strip()
  
  commit_messages = get_commit_message(since=since, repo_dir=repo_dir)
  response = completion(
    model="gpt-4o-mini",  
    messages=[
      {"role": "system",
      "content": ("Here are the commit messages from the user. "
                  "First, summarize the messages with one bullet point a day, even it there are multiple messages on the same day. "
                  "For each day, mark the date at the beginning of the bullet point, the format is 'YYYY-MM-DD'. "
                  "Title this section as 'Daily works'"
                  "Second, provide a short summary to help the user remember what they were at."
                  "Title this section as 'Summary'"
                  "Be concise, use short sentences. Focus on the work itself, avoid using 'You' in the summary. "
                  f"\n\n{commit_messages}")}]
  )

  resp = response.choices[0].message.content # type: ignore
  return resp