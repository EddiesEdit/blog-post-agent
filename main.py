from dotenv import load_dotenv
load_dotenv()

import asyncio
from google.adk.runners import InMemoryRunner
from agent import blog_post_agent
from rich.console import Console
from rich.markdown import Markdown
console = Console()

def extract_final_text(response):
    """
    Extract only the final readable text from ADK events.
    """
    final_text = None

    for event in response:
        if not event.content:
            continue

        for part in event.content.parts:
            # Only keep normal text (ignore function calls / metadata)
            if getattr(part, "text", None):
                final_text = part.text  # keep overwriting until last

    return final_text


async def main():
    runner = InMemoryRunner(agent=blog_post_agent)
    response = await runner.run_debug(
        "Write a blog post about the benefits of multi-agent systems for software developers"
    )
            



    final_answer = extract_final_text(response)

    #print("\n=== FINAL ANSWER ===\n")
    console.print(Markdown(final_answer))
    #print(final_answer)


if __name__ == "__main__":
    asyncio.run(main())
