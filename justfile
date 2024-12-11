
docs:
    sphinx-autobuild docs/source docs/build/html

test:
    # Works only on Rasperry Pi
    pytest
