
python run.py localhost 8080 tests/config.json &
PID=$!
sleep 3
python tests/_test_server.py
kill $PID

