# Bitly Coding Challenge ReadMe
By Cache McClure

This challenge was completed using Python 3.11. However, none of the included functions are strictly dependent on that version.

## Included Files
* Problem outline in `data_eng_challenge.md` file
* Data files located in `data` directory
  * Click data in `decodes.json`
  * Link encoding data in `encodes.csv`
* Solution functions in `solutions` directory
  * Fast and rough first pass at solution in `fast.py`
  * Comprehensive approach including optimizations and methodology for streamed data in `comprehensive.py`
* Test functions in `tests` directory
  * Test data is stored in the `test_data_*` files
  * Unit tests stored in `test_solution.py` file and executed automatically during the Docker build step
  * If no tests fail, the Docker build step will complete correctly. If a test fails, it will raise an error during the build step
* Primary entry path including execution and performance evaluations in `main.py`
* Output of final solution in `final_output.json`
* Module requirements in `requirements.txt`
* Docker build instruction in `Dockerfile` (just run `docker build -t [username]/[docker-image-name]:latest .`)

## Solutions
I included two solutions for this challenge. The first is a fast and dirty approach I would use for a task that doesn't need to be 
stable, scalable, or particularly testable. It's more of a rapid prototyping approach for a quick solution that works once
and doesn't need to be used again. The second solution is more of a comprehensive solution which breaks the process into multiple
functions and focuses more on efficiency, testability, scalability, and applicability. The process is geared more toward a
streaming or batch processing environment (depending on how certain functions are implemented) and utilizes built-in libraries
rather than including external dependencies.

When you run the Docker image, you'll see that both methods are included in the output. They should both be the same, but there
is an efficiency measure posted for each (in this case, a simple performance timer but the memory usage was also significantly
better for the comprehensive solution in testing). The output from the comprehensive step is also saved in the file named 
`final_output.json` in the `/code` directory on the Docker image in addition to being printed in the console.

If you want to run this without building the Docker image, run the following two commands (assuming you have Python 3 installed):

    python -m pip install -r requirements.txt
    python main.py
Or if you're using a Mac:

    python3 -m pip install -r requirements.txt
    python3 main.py
To run the tests manually, please use:

    python -m unittest tests/test_solution.py