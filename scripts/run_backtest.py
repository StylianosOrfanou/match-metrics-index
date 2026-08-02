from validation.backtest_runner import (
    BacktestRunner,
)


def run_backtest(
    repository,
    predictor,
):
    fixtures = repository.load()

    runner = BacktestRunner(
        predictor=predictor,
    )

    return runner.run(
        fixtures,
    )


if __name__ == "__main__":
    raise SystemExit(
        "Use run_backtest() from the application "
        "composition root."
    )