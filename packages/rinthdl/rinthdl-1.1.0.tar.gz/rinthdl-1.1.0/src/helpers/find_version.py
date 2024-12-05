RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"
def find_version(versions, project_version, min_version_type):
    """
    Fetches either the latest or specified version from a list of versions.

    Args:
        versions (list): List of versions.
        project_version (str): Project version.
        min_version_type (str): release, beta or alpha.

    Returns:
        dict: Latest or specified version.
    """
    if not versions or type(versions) is str:
        return f"❌ Versions list is empty"

    if project_version:
        for version in versions:
            if version.get("version_number") == project_version:
                return version
        project_id = versions[0].get("project_id")
        return f"❌ No version found matching {project_version} ➜ {BLUE}https://modrinth.com/project/{project_id}{RESET}"

    if min_version_type:
        valid_version_types = ["release", "beta", "alpha"]

        if min_version_type not in valid_version_types:
            return f"❌ Unrecognized channel. Choose between 'release', 'beta' or 'alpha'."

        start_index = valid_version_types.index(min_version_type)
        preferred_types = valid_version_types[:start_index + 1]

        for version_type in preferred_types:
            for version in versions:
                if version.get("version_type") == version_type:
                    return version

        project_id = versions[0].get("project_id")
        return f"❌ No version found matching {min_version_type} ➜ {BLUE}https://modrinth.com/project/{project_id}{RESET}"

    return versions[0]
