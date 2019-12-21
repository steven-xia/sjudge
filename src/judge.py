import shlex
import subprocess
import sys
import time
import typing

TEST_IO_TYPE: typing.Type = typing.Iterable[str]

TESTCASE_TYPE: typing.Type = typing.Iterable[
    typing.Tuple[TEST_IO_TYPE, TEST_IO_TYPE]
]

ANSWER_CORRECT = "Answer Correct"
RUNTIME_ERROR = "Runtime Error"
TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
WRONG_ANSWER = "Wrong Answer"


class TestcaseResult:
    def __init__(self, given_input: TEST_IO_TYPE, given_output: TEST_IO_TYPE,
                 received_output: TEST_IO_TYPE, error_message: TEST_IO_TYPE,
                 exitcode: int = False, time_for_test: float = 0,
                 time_limit_exceeded: bool = False) -> None:
        self.given_input: TEST_IO_TYPE = given_input
        self.given_output: TEST_IO_TYPE = given_output
        self.received_output: TEST_IO_TYPE = received_output
        self.error_message: TEST_IO_TYPE = error_message
        self.exitcode: int = exitcode
        self.time_for_test: float = time_for_test
        self.time_limit_exceeded: bool = time_limit_exceeded

        self.verdict: str = self._get_verdict()
        self.passed: bool = self.verdict == ANSWER_CORRECT

    def _get_verdict(self) -> str:
        if self.time_limit_exceeded:
            return TIME_LIMIT_EXCEEDED
        elif self.exitcode:
            return RUNTIME_ERROR
        elif self.received_output != self.given_output:
            return WRONG_ANSWER
        else:
            return ANSWER_CORRECT


class JudgeResult:
    def __init__(self) -> None:
        self.testcases: typing.List[TestcaseResult] = []

        self.passed_testcases: int = 0
        self.total_testcases: int = 0
        self.maximum_time: float = 0.0

    def __add__(self, other: TestcaseResult) -> "JudgeResult":
        self.add_result(other)
        return self

    def __getitem__(self, item: int) -> TestcaseResult:
        return self.testcases[item]

    def __iter__(self) -> iter:
        return iter(self.testcases)

    def add_result(self, tc: TestcaseResult) -> None:
        self.testcases.append(tc)

        self.passed_testcases += tc.passed
        self.total_testcases += 1
        self.maximum_time = max(self.maximum_time, tc.time_for_test)


def judge_file(file_command: str, testcases: TESTCASE_TYPE,
               time_limit: float = 1.0) -> JudgeResult:
    result_tracker = JudgeResult()

    for test_number, (test_input, test_output) in enumerate(testcases):
        start_time = time.time()

        try:
            process_return = subprocess.run(
                shlex.split(file_command),
                input=_encode_io(test_input),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=time_limit,
                universal_newlines=True
            )

            process_output = _decode_io(process_return.stdout)
            process_errors = _decode_io(process_return.stderr)
            process_exitcode = process_return.returncode

            result_tracker += TestcaseResult(
                test_input, test_output, process_output, process_errors,
                process_exitcode, time_for_test=1000 * (time.time() - start_time)
            )

        except subprocess.TimeoutExpired as ex:
            result_tracker += TestcaseResult(
                test_input, test_output, [""], [""], 1,
                time_for_test=1000 * ex.timeout,
                time_limit_exceeded=True
            )

        finally:
            elapsed_time = 1000 * (time.time() - start_time)
            elapsed_time = min(1000 * time_limit, elapsed_time)

            this_result = result_tracker[-1]
            _display("Case #{} → {}  [{} ms]".format(
                test_number + 1,
                this_result.verdict,
                round(elapsed_time)
            ))

            if this_result.verdict == RUNTIME_ERROR:
                _display("\n".join(
                    f"  - {s}" for s in this_result.error_message
                ))
                _display("  - Process finished with exit code {}".format(
                    this_result.exitcode
                ))

            elif this_result.verdict == WRONG_ANSWER:
                _display("  - Expected output:")
                _display("\n".join(
                    f"  - {s}" for s in this_result.given_output
                ))

                _display("  - Received output:")
                _display("\n".join(
                    f"  - {s}" for s in this_result.received_output
                ))

    _display("Final score: {}/{}  [{} ms]".format(
        result_tracker.passed_testcases,
        result_tracker.total_testcases,
        round(result_tracker.maximum_time)
    ))
    return result_tracker


def _encode_io(given_io: TEST_IO_TYPE) -> str:
    return "".join(
        f"{input_line}\n" for input_line in given_io
    )


def _decode_io(process_io: str) -> TEST_IO_TYPE:
    return [
        s.strip("".join(['\r', '\n']))
        for s in process_io.strip().split("\n")
    ]


def _display(s: str) -> None:
    sys.stdout.write(f"{s}\n")
    sys.stdout.flush()