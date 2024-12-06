from poisson_d.concurrent import run


def sample_task() -> str:
    return "Task completed"


def test_run():
    tasks = [
        ("Task 1", sample_task),
        ("Task 2", sample_task),
        ("Task 3", sample_task),
    ]

    results = run(tasks)

    assert results == {
        "Task 1": "Task completed",
        "Task 2": "Task completed",
        "Task 3": "Task completed",
    }
