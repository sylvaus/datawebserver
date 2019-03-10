"""
This script must be run to compile and bundle all the ts files into a bundle file
"""
import os
from glob import glob
from subprocess import run

if __name__ == '__main__':
    # Compile files
    run(["tsc"], shell=True)

    # Bundle all the files
    generated_files = glob(os.path.join(".", "static", "ts", "*.js"))
    run(["browserify"] + generated_files + ["-o", "static/js/bundle.js"], shell=True)
