from typing import Annotated
import typer
import archimate.pipeline

app = typer.Typer()

@app.command()
def step1():
    archimate.pipeline.step1()

@app.command()
def step2():
    archimate.pipeline.step2()

@app.command()
def step2_diagrams(max_diagrams: Annotated[int, typer.Option(help="Set maximum amount of diagrams to generate.")] = None):
    archimate.pipeline.step2_diagrams(max_diagrams)

@app.command()
def step3():
    archimate.pipeline.step3()

if __name__ == "__main__":
    app()