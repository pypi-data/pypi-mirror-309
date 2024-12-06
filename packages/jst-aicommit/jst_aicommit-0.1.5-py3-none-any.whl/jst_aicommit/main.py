from .blackbox import Blackbox
from .git import Git
import questionary
from rich import print


class JstAiCommit:

    def __init__(self) -> None: ...

    def run(self):
        """Ish tushurovchi funcsiya"""
        ai = Blackbox()
        git = Git()
        status, changes = git.diff()
        if not status or len(changes.strip()) == 0:
            print("[red bold] No changes to commit.[/red bold]")
            exit()
        try:
            commit = questionary.text("commit: ", default=ai.get_commit(changes)).ask()
        except Exception as e:
            print("[red bold]AI yordamida commit yaratishda xatolik yuz berdi[/red bold]")
        git.commit(commit)


def main():
    """Main funcsiya"""
    obj = JstAiCommit()
    obj.run()
