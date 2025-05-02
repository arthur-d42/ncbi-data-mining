{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python312;
in pkgs.mkShell {
  buildInputs = with pkgs; [
    python
    python.pkgs.pip
    python.pkgs.setuptools
    python.pkgs.wheel
    
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
    export C_INCLUDE_PATH="${pkgs.zlib.dev}/include:${pkgs.blas}/include"
    export LIBRARY_PATH="${pkgs.zlib}/lib:${pkgs.blas}/lib"
    
    # Make sure pip is up to date
    pip install --upgrade pip setuptools wheel
    
    # Install from requirements.txt if it exists
    if [ -f "requirements.txt" ]; then
      echo "Installing packages from requirements.txt..."
      pip install -r requirements.txt
      
      # Test imports for key packages
      echo "Testing imports..."
      if grep -q "numpy" requirements.txt; then
        python -c "import numpy; print('✓ NumPy imported successfully')" || echo "✗ NumPy import failed"
      fi
      if grep -q "pandas" requirements.txt; then
        python -c "import pandas; print('✓ Pandas imported successfully')" || echo "✗ Pandas import failed"
      fi
      if grep -q "networkx" requirements.txt; then
        python -c "import networkx; print('✓ NetworkX imported successfully')" || echo "✗ NetworkX import failed"
      fi
      if grep -q "py2cytoscape" requirements.txt; then
        python -c "import py2cytoscape; print('✓ py2cytoscape imported successfully')" || echo "✗ py2cytoscape import failed"
      fi
      
      echo "All packages from requirements.txt installed and tested!"
    else
      echo "No requirements.txt found. Installing default packages..."
      pip install numpy pandas networkx py2cytoscape
      
      # Test imports for default packages
      echo "Testing imports..."
      python -c "import numpy; print('✓ NumPy imported successfully')" || echo "✗ NumPy import failed"
      python -c "import pandas; print('✓ Pandas imported successfully')" || echo "✗ Pandas import failed"
      python -c "import networkx; print('✓ NetworkX imported successfully')" || echo "✗ NetworkX import failed"
      python -c "import py2cytoscape; print('✓ py2cytoscape imported successfully')" || echo "✗ py2cytoscape import failed"
      
      echo "Default packages installed and tested!"
    fi
    
    echo ""
    echo "Python development environment ready!"
    echo "Python: $(which python) ($(python --version))"
    echo "Pip: $(which pip) ($(pip --version))"
    echo "Virtual environment: $VIRTUAL_ENV"
    echo ""
    echo "You can now work with your Python packages."
  '';
}