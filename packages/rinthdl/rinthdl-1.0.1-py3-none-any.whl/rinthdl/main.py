from helpers.fetch_project_id_from_slug import check_project as fetch_id
from helpers.fetch_versions import fetch_versions
from helpers.find_version import find_version
from helpers.find_dependencies import find_dependencies
from helpers.find_project_meta import find_project_meta
from helpers.download import find_url, download_file, validate_path

import argparse
import json

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

def get_id(slug):
    project_id = fetch_id(slug)
    if project_id.startswith("❌"):
        print(project_id)
        exit(1)
    return project_id

def get_versions(project_id, game_version, platform):
    versions = fetch_versions(project_id, game_version, platform)
    if type(versions) != list:
        print(versions)
        exit(1)
    return versions

def get_version(project_id, game_version, platform, project_version):
    versions = get_versions(project_id, game_version, platform)
    version = find_version(versions, project_version)
    if type(version) != dict:
        print(version)
        exit(1)
    return version

def main():
    parser = argparse.ArgumentParser(description='Fetch all versions of a project.')
    parser.add_argument('operation', help='What do you want to do?')
    parser.add_argument('slug', help='The project slug.')
    parser.add_argument('--game_version', help='The game version.')
    parser.add_argument('--platform', help='The platform.')
    parser.add_argument('--project_version', help='The project version.')
    parser.add_argument('--path', help='The path to download to.')

    args = parser.parse_args()
    slug = args.slug
    game_version = args.game_version
    platform = args.platform
    project_version = args.project_version
    path = args.path

    match args.operation:
        case 'get_id':
            project_id = get_id(slug)
            print(f"Project ID of {slug}: {GREEN}{project_id}{RESET}")
        case 'get_versions':
            project_id = get_id(slug)
            versions = get_versions(project_id, game_version, platform)
            print(json.dumps(versions, indent=4))
        case 'get_version':
            project_id = get_id(slug)
            version = get_version(project_id, game_version, platform, project_version)
            print(json.dumps(version, indent=4))
        case 'get_dependencies':
            project_id = get_id(slug)
            version = get_version(project_id, game_version, platform, project_version)
            dependencies = find_dependencies(version)
            if not dependencies:
                print("✔️ No dependencies found")
            else:
                print("Following dependencies were found:")
                for dep in dependencies:
                    print(f"{BLUE}https://modrinth.com/project/{dep}{RESET}")
        case 'get_project_meta':
            project_id = get_id(slug)
            meta = find_project_meta(project_id)
            print(f"Type: {meta[0].capitalize()}")
            print("Loaders:", end=" ")
            for loader in meta[1]:
                print(f"{loader.capitalize()}", end=" ")
            print(f"\nSlug: {meta[2]}")
        case 'download':
            if not path:
                print("❌ Please provide a path")
                exit(1)

            validate_path(path)
            project_id = get_id(slug)
            version = get_version(project_id, game_version, platform, project_version)

            result = find_url(version)
            if not type(result) == tuple:
                print(f"{RED}{result}{RESET}")
                exit(1)
            url, filename = result

            if download_file(url, filename, path):
                print(f"✔️ Successfully downloaded: {GREEN}{filename}{RESET}.")
            else:
                print(f"❌ An Error occurred during the download of {filename}")

if __name__ == '__main__':
    main()
