"""app package."""
import os

from app.settings import settings


def set_aws_credentials_and_region(
    access_key, secret_key, region_name, profile_name="default"
):
    """Set AWS credentials and region directly to ~/.aws/credentials
    and ~/.aws/config."""

    # Ensure the .aws directory exists
    aws_dir = os.path.expanduser("~/.aws")
    if not os.path.exists(aws_dir):
        os.makedirs(aws_dir)

    # Write the credentials to ~/.aws/credentials
    credentials_file = os.path.join(aws_dir, "credentials")
    with open(credentials_file, "w") as f:
        f.write(f"[{profile_name}]\n")
        f.write(f"aws_access_key_id = {access_key}\n")
        f.write(f"aws_secret_access_key = {secret_key}\n")

    # Write the region to ~/.aws/config
    config_file = os.path.join(aws_dir, "config")
    with open(config_file, "w") as f:
        f.write(
            f"[profile {profile_name}]\n"
            if profile_name != "default"
            else "[default]\n"
        )
        f.write(f"region = {region_name}\n")


if settings.ENVIRONMENT != "development":
    set_aws_credentials_and_region(
        settings.AWS_ACCESS_KEY,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AWS_REGION,
        profile_name="default",
    )
