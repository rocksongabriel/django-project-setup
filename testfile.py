from rich.progress import Progress


with Progress() as progress:
    advance = True
    task = progress.add_task("Install Package", total=100)
    while advance:
        for i in range(0, 10000000000):
            progress.advance(task)
        advance = False