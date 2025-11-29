

# ai_value_auditor/__main__.py
"""
Command-line interface for the AI Value Auditor system.
"""

import argparse
import sys
from .server import start_server

def main():
    parser = argparse.ArgumentParser(description="AI Value Auditor System")
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0", 
        help="Host to run the server on"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to run the server on"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    args = parser.parse_args()
    
    print(f"Starting AI Value Auditor server on {args.host}:{args.port}")
    start_server(host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()
