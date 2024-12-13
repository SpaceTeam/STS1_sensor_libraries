
docs:
    sphinx-autobuild docs/source docs/build/html

clean_docs:
    cd docs && make clean

test:
    # Works only on Rasperry Pi
    uv run pytest
