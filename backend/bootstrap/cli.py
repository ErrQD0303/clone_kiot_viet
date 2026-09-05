"""Application command-line entry point."""

import argparse
import asyncio

from bootstrap.container import create_application_container
from bootstrap.rbac_manifest import APPLICATION_RBAC
from identity.application.service.admin_init_service import AdminInitService
from identity.application.service.sync_rbac_service import SyncRbacService


async def sync_rbac_command() -> None:
	"""Synchronize the application RBAC manifest with the database."""
	container = create_application_container()

	try:
		service: SyncRbacService = await container.sync_rbac_service()
		result = await service.execute(APPLICATION_RBAC)
		print(
			"RBAC synchronized:",
			f"\n\tpermissions created={result.permissions_created},",
			f"\n\tpermissions updated={result.permissions_updated},",
			f"\n\troles created={result.roles_created},",
			f"\n\tgrants added={result.grants_added}",
		)
	finally:
		await container.shutdown_resources()

async def admin_init_command() -> None:
	"""Initialize the admin user and role in the database."""
	container = create_application_container()

	try:
		service: AdminInitService = await container.admin_init_service()
		result = await service.execute(APPLICATION_RBAC)
		print(
			"RBAC synchronized:",
			f"\n\tpermissions created={result.permissions_created},",
			f"\n\tpermissions updated={result.permissions_updated},",
			f"\n\troles created={result.roles_created},",
			f"\n\tgrants added={result.grants_added}",
			f"\n\tadmin user created={result.user_created}",
			f"\n\tadmin role granted={result.role_granted}",
		)
	finally:
		await container.shutdown_resources()


def main() -> None:
	"""Parse and execute an application command."""
	parser = argparse.ArgumentParser(description="Application management commands")
	subcommands = parser.add_subparsers(dest="command", required=True)
	subcommands.add_parser("sync-rbac", help="Synchronize roles and permissions")
	subcommands.add_parser("admin-init", help="Initialize the admin user and role")
	args = parser.parse_args()

	match args.command:
		case "sync-rbac":
			asyncio.run(sync_rbac_command())
		case "admin-init":
			asyncio.run(admin_init_command())
		case _:
			parser.print_help()

if __name__ == "__main__":
	main()
