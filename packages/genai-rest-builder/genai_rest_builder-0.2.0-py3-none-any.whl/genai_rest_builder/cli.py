# cli.py
import click
from genai_rest_builder import genai_langserve_codegen


@click.command()
def create_gen_ai_project_structure():
    genai_langserve_codegen.main()


if __name__ == "__main__":
    create_gen_ai_project_structure()
