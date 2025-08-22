import os
import sys

# Get the correct path to the workspace
workspace_path = r"vscode-vfs://github%2B7b2276223a312c22726566223a7b2274797065223a342c226964223a226d6173746572227d7d/GmailHelene/aksjeny2"

# Test the sentiment route
print("Testing sentiment route...")
try:
    # Change to the correct directory
    os.chdir(workspace_path.replace("vscode-vfs://", "").replace("%2B", "+").replace("%22", '"').replace("%7b", "{").replace("%7d", "}").replace("%3a", ":"))
    
    # Add the current directory to the Python path
    sys.path.insert(0, os.getcwd())
    
    from app.routes.analysis import sentiment
    print("✓ Sentiment route imported successfully")
    
except Exception as e:
    print(f"✗ Error importing sentiment: {e}")
    import traceback
    traceback.print_exc()
