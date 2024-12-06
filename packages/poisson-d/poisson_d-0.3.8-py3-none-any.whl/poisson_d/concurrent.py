import threading as m
from typing import List, Dict, Callable
from rich.console import Console
import queue as q

console = Console()


def worker(name: str, exectuion: Callable, queue: q.Queue):
    """Function to be run in a separate process."""
    result = exectuion()
    queue.put((name, result))


def run(tasks: List[tuple[str, Callable]], timeout_sec: float = 60.0) -> Dict[str, any]:
    processes: List[m.Thread] = []
    queue = q.Queue(maxsize=10)

    for task in tasks:
        name, execution = task
        p = m.Thread(target=worker, args=(name, execution, queue), name=name)
        processes.append(p)
        p.start()

    for p in processes:
        p.join(timeout=timeout_sec)

    results = {}
    while not queue.empty():
        name, result = queue.get(timeout=1)
        results[name] = result

    return results
