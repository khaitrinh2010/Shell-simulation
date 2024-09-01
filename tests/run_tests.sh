#!/bin/bash

# Your testing script here!
program="python3 $HOME/mysh.py"
TEST_DIR="${HOME}/tests/io_files"
count=0
for test in "${TEST_DIR}"/*.in; do
    basename=$(basename "$test" .in)
    expected="${TEST_DIR}/${basename}.out"

    $program < "$test" > "$TEST_DIR/$basename.actual" 2>&1
    out="$TEST_DIR/$basename.actual"

    if diff -q "$expected" "$out" > /dev/null; then
        echo "PASS ${basename}"
        count=$((count+1))
    else
        echo "FAIL ${basename}"
        echo "Expected"
        cat "$expected"
        echo "Actual" 
        cat "$out"
    fi
done
echo "$count out of 15 tests passed"
