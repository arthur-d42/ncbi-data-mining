{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python312;
  pyscript = pkgs.writeScriptBin "pyscript" ''
    #!/usr/bin/env bash
    source ${builtins.toString ./.}/.venv/bin/activate
    python "$@"
  '';
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python
    python.pkgs.pip
    python.pkgs.setuptools
    python.pkgs.wheel
    
    # Add our custom script
    pyscript
    
    # System libraries
    stdenv.cc.cc.lib
    zlib
    blas
    lapack
    
    # Development tools
    gcc
    gnumake
    pkg-config
  ];
  
  shellHook = ''
    # Create a fresh venv
    if [ ! -d ".venv" ]; then
      ${python}/bin/python -m venv .venv
      echo "Created new virtual environment"
    else
      echo "Using existing virtual environment"
    fi
    
    source .venv/bin/activate
    
    # Set up library paths for compiled extensions
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      pkgs.blas
      pkgs.lapack
    ]}:$LD_LIBRARY_PATH
    
    # Set compiler flags for building binary extensions
    export CFLAGS="-I${pkgs.zlib.dev}/include -I${pkgs.blas}/include"
    export LDFLAGS="-L${pkgs.zlib}/lib -L${pkgs.blas}/lib"
    
    # Make sure pip is up to date
    pip install --upgrade pip setuptools wheel
    
    # Install from requirements.txt if it exists
    pip install -r requirements.txt
    echo ""
    echo "Python development environment ready!"
    echo "Python: $(which python) ($(python --version))"
    echo "Pip: $(which pip) ($(pip --version))"
    echo "Virtual environment: $VIRTUAL_ENV"
    echo ""
    echo "To run scripts directly, use: pyscript your_script.py"
    echo "This ensures the script runs with all dependencies available."
  '';
}