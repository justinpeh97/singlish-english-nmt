#!/bin/bash

CURRENT="$PWD"
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

mkdir -p "$ROOT/third-party"
cd "$ROOT/third-party"
git clone 'https://github.com/artetxem/phrase2vec.git'