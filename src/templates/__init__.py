from pathlib import Path

from promplate import Node, Template

ROOT = Path(__file__).parent.resolve()


prompt = Node.read(ROOT / "prompt.j2")

messages = Template.read(ROOT / "messages.j2")
response = Template.read(ROOT / "response.j2")
