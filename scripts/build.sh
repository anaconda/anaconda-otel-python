#!/bin/bash
# SPDX-FileCopyrightText: 2025 Anaconda, Inc
# SPDX-License-Identifier: Apache-2.0

python=`which python`
[[ -z "${python}" ]] && python=`which python3`

# Bash function definitions.
function mac_install_latex() {
    # Install LaTeX on MacOS
    local found=`brew list --cask | grep mactex`
    [[ -z "${found}" ]] && brew install --cask mactex && return $?
    echo "Latex for MacOS is already installed!"
    return 0
}

function linux_install_latex() {
    # Install LaTeX on Linux
    local found=`apt list | grep latexmk 2>/dev/null`
    [[ -z "${found}" ]] && sudo apt-get install -y texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended latexmk && return $?
    echo "Latex for Sphinx is already installed!"
    return 0
}

function windows_install_latex() {
    # Install LaTeX on Windows
    echo "ERROR: Windows unsupported for PDF builds!" >&2
    exit -1  # Return Error Code
}

function install_latex() {
    # Install LaTeX based on the operating system
    case $UNAME in
        Darwin)
            mac_install_latex
            ;;
        Linux)
            linux_install_latex
            ;;
        MINGW*|MSYS*)
            windows_install_latex
            [[ $? -ne 0 ]] && exit -1  # Return Error Code (Windows currently not supported)
            ;;
        *)
            echo "ERROR: Unsupported OS!" >&2
            exit -1
            ;;
    esac
    return $?
}

function pip_exists() {
    # Check if a pip package exists
    local found=`pip3 list | awk '{print $1}' | grep -e "^$1$"`
    if [ -z "$found" ]; then
        return 1
    else
        return 0
    fi
}

function pip_install() {
    for pkg in setuptools build wheel Sphinx sphinx-rtd-theme myst-parser; do
        pip_exists $pkg
        if [ $? -ne 0 ]; then
            echo "Installing $pkg..."
            pip3 install $pkg
        else
            echo "$pkg already installed."
        fi
    done
}

function git_version() {
    local full=`git describe --tags --long --match 'v[0-9]*'`
    IFS='-' read -ra parts <<< "${full}"

    local version=`echo ${parts[0]} | sed 's/^v//g'`
    [[ "${#parts[@]}" == "3" ]] && version="${version}.dev${parts[1]}"
    echo "${version}"
}

function replace_version() {
    sed -i.bak "s/__SDK_VERSION__ = \\\"1.0.0\\\"/__SDK_VERSION__ = \"${1}\"/g" anaconda_opentelemetry/__version__.py
}

function restore_version() {
    rm anaconda_opentelemetry/__version__.py
    mv anaconda_opentelemetry/__version__.py.bak anaconda_opentelemetry/__version__.py
}

# Set global variables
UNAME=`uname`
export __SDK_VERSION__="$(git_version)"
echo ${__SDK_VERSION__} >version.txt
replace_version "${__SDK_VERSION__}"

# Install dependencies if needed
CONDA=`which conda`
[[ -z "${CONDA}" ]] && echo "ERROR: conda not found! Please install the latest version of miniconda from https://anaconda.com/." >&2 && restore_version && exit 1
install_latex
pip_install

# Clean up previous builds and prepare for new build
rm -rf *.egg-info dist docs/build docs/source/*.rst conda-recipe/build .pytest_cache anaconda-opentelemetry/__pycache__ tests/__pycache__ docs/source/__pycache__
mkdir dist

# Adjust paths to find Sphinx and its dependencies
LOCATION=`pip3 show sphinx | grep "^Location" | awk '{print $2}'`
BIN="${LOCATION}/../../../bin"
export PYTHONPATH="${LOCATION}/:$PYTHONPATH"
export PATH="${BIN}:$PATH"

# Generate and modify API docs.
sphinx-apidoc -o docs/source anaconda_opentelemetry
rm -f docs/source/modules.rst
[[ $? -ne 0 ]] && echo "ERROR: sphinx-apidoc build failed!" >&2 && restore_version && exit 1

lines=`wc -l docs/source/anaconda-opentelemetry.rst | awk '{print $1}'`
need=`expr $lines - 7`
head -n ${need} docs/source/anaconda-opentelemetry.rst >/tmp/rst.tmp
rm -f docs/source/anaconda-opentelemetry.rst
mv /tmp/rst.tmp docs/source/anaconda-opentelemetry.rst

# Build the documentation
cd docs
rm -rf build
sphinx-build -M html "source" "build"
[[ $? -ne 0 ]] && echo "ERROR: sphinx build failed to produce HTML output!" >&2 && restore_versiobnt && exit 1
sphinx-build -M latexpdf "source" "build"
[[ $? -ne 0 ]] && echo "ERROR: sphinx build failed to produce PDF output!" >&2 && restore_version && exit 1
cd ..

# Copy documentation to the 'dist' folder
tar -caf dist/anaconda-opentelemetry-${__SDK_VERSION__}-html-doc.tar.gz docs/build/html
cp docs/build/latex/anacondaopentelemetrywrapper.pdf dist/anaconda-opentelemetry-${__SDK_VERSION__}.pdf

# Produce conda package
conda build --output-folder ./conda-recipe/build conda-recipe
[[ $? -ne 0 ]] && echo "ERROR: conda build failed!" >&2 && restore_version && exit 1
restore_version

cp conda-recipe/build/noarch/anaconda-opentelemetry-${__SDK_VERSION__}-py_0.conda dist/

# Clean up generated files
rm -rf docs/source/anaconda*opentelemetry.rst version.txt

# Clean exit...
echo
echo "**********************************************"
echo "*** All collateral is in folder 'dist'."
