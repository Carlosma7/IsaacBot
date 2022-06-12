# ----------MACROS-----------
BIN= bin

# ---------- ALL ------------
all: setup run clean

# ---------- SETUP ----------
setup:
	pip3 install -r requirements.txt

# ---------- RUN ------------
run:
	python3 src/isaacbot.py

# ---------- CLEAN ----------
clean:
	find . -maxdepth 5 -type d -name __pycache__ -exec rm -r {} +

.Phony: setup run clean
