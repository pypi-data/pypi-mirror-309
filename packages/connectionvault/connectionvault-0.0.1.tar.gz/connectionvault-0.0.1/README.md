# ConnectionVault

# Navigate to your project directory
cd /path/to/your/project

# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
# venv\Scripts\activate  # For Windows

# Install Poetry inside the virtual environment
pip install poetry

# Initialize the Poetry project if not already done
poetry init

# Add dependencies
poetry add requests

# Build the project
poetry build
