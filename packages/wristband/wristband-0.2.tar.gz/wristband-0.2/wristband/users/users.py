# users.py

import argparse
import sys
from users_utils import UsersService
from wristband.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    get_non_empty_response,
)


def main():
    parser = argparse.ArgumentParser(description="Users Service Command-Line Interface")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Sub-command: create_input_user_csv
    subparsers.add_parser('create_input_user_csv', help='Create an input CSV template for users')

    # Sub-command: upload_user_csv
    parser_upload = subparsers.add_parser('upload_user_csv', help='Upload users from CSV')
    parser_upload.add_argument('--token', type=str, help='Authentication token')
    parser_upload.add_argument('--application_vanity_domain', type=str, help='Application vanity domain')
    parser_upload.add_argument('--tenant_id', type=str, help='Tenant ID')
    parser_upload.add_argument('--identity_provider_name', type=str, help='Identity provider name')
    parser_upload.add_argument('--invite_users', action='store_true', help='Invite users after creation')

    # Parse arguments
    args = parser.parse_args()

    # Check if a command is provided
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'create_input_user_csv':
        # Initialize service without credentials
        service = UsersService()
        service.create_input_user_csv()
    elif args.command == 'upload_user_csv':
        # Ensure required arguments are provided
        required_args = ['token', 'application_vanity_domain', 'tenant_id', 'identity_provider_name']
        missing_args = [arg for arg in required_args if getattr(args, arg) is None]
        if missing_args:
            print(f"Missing required arguments for command '{args.command}': {', '.join(missing_args)}")
            parser_upload.print_help()
            sys.exit(1)

        # Initialize the service
        service = UsersService(
            token=args.token,
            application_vanity_domain=args.application_vanity_domain,
            tenant_id=args.tenant_id,
            identity_provider_name=args.identity_provider_name
        )

        # Execute the upload_user_csv method
        try:
            logs = service.upload_user_csv(invite_users=args.invite_users)
            for log in logs:
                print(log)
        except (AuthenticationError, AuthorizationError, BadRequestError) as e:
            print(f"Error: {e}")
    else:
        print(f"Unknown command '{args.command}'")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()