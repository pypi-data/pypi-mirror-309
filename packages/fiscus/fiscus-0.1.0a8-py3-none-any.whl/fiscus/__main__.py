# fiscus/__main__.py

import argparse
import json  # Needed to handle JSON input for parameters
from fiscus import FiscusClient, __version__, __description__

def main():
    # Set up the argument parser with a brief description of the CLI
    parser = argparse.ArgumentParser(description="Fiscus SDK Command-Line Interface")

    # Add argument for displaying SDK information
    parser.add_argument(
        '--info',
        action='store_true',
        help="Show SDK information"
    )

    # Add argument for executing a sample operation with required parameters
    parser.add_argument(
        '--execute',
        metavar=('CONNECTOR', 'OPERATION', 'PARAMS'),
        nargs=3,
        help="Execute a sample operation. Provide CONNECTOR, OPERATION, and PARAMS in JSON format."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Handle the `--info` argument to display SDK information
    if args.info:
        print("Fiscus SDK -", __description__)  # Dynamic description from __init__.py
        print("Version:", __version__)          # Dynamic version from __init__.py
        print("For more information, visit the Fiscus SDK documentation.")
    
    # Handle the `--execute` argument to perform an operation
    elif args.execute:
        connector, operation, params_json = args.execute

        try:
            # Parse the params argument as JSON
            params = json.loads(params_json)

            # Initialize FiscusClient with a placeholder API key
            client = FiscusClient(api_key='YOUR_FISCUS_API_KEY')
            
            # Execute the operation with the specified connector, operation, and parameters
            response = client.execute(connector, operation, params)

            # Check if the operation was successful and print the result or error message
            if response.success:
                print("Operation successful:", response.result)
            else:
                print("Operation failed:", response.error_message)
        
        # Handle JSON parsing errors and any other exceptions that may occur
        except json.JSONDecodeError:
            print("Error: Parameters must be valid JSON.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Display help message if no valid command is provided
    else:
        print("No command specified. Use --help for a list of available commands.")

# Entry point to run the main function when script is executed as a module
if __name__ == '__main__':
    main()
