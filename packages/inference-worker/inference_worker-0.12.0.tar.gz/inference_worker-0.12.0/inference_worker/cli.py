import os
import shutil
import click, pathlib
from .core.worker import Worker

@click.group()
def worker():
    pass

@worker.command()
def init():
    """Initialize boilerplate files for custom implementation."""
    sourceDir = pathlib.Path(__file__).parent / 'boilerplate'

    configFilePath = sourceDir / 'config.json'
    envFilePath = sourceDir / '.env'
    implementationDirPath = sourceDir / 'implementation'

    destinationDir = pathlib.Path(os.getcwd())

    if not os.path.exists(str(destinationDir)):
        os.makedirs(str(destinationDir), exist_ok=True)

    
    shutil.copy(str(configFilePath), str(destinationDir / 'config.json'))
    shutil.copy(str(envFilePath), str(destinationDir / '.env'))
    shutil.copytree(implementationDirPath, os.path.join(os.getcwd(), 'implementation'))
    print(f"Boilerplate created at {str(destinationDir)}/implementation")

@worker.command()
def start():
    worker = Worker()
    try:
        worker.start_consuming()
    except Exception as e:
        print(e)
        worker.close()

if __name__ == '__main__':
    worker()
