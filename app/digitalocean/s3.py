import boto3
import mimetypes
from config import Settings

env = Settings()


def get_spaces_client(**kwargs):
    """
    :param kwargs:
    :return:
    """
    region_name = kwargs.get("region_name")
    endpoint_url = kwargs.get("endpoint_url")
    key_id = kwargs.get("key_id")
    secret_access_key = kwargs.get("secret_access_key")

    session = boto3.session.Session()

    return session.client(
        "s3",
        region_name=region_name,
        endpoint_url=endpoint_url,
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_access_key,
    )


def blob_exists(spaces_client, space_name, blob_name):
    """
    :param spaces_client: Your DigitalOcean Spaces client from get_spaces_client()
    :param space_name: Unique name of your space. Can be found at your digitalocean panel
    :param blob_name: Name of your blob
    :return:
    """
    try:
        spaces_client.head_object(Bucket=space_name, Key=blob_name)
        return True
    except spaces_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise e


def upload_file_to_space(spaces_client, space_name, file_src, save_as, **kwargs):
    """
    :param spaces_client: Your DigitalOcean Spaces client from get_spaces_client()
    :param space_name: Unique name of your space. Can be found at your digitalocean panel
    :param file_src: File location on your disk
    :param save_as: Where to save your file in the space
    :param kwargs
    :return:
    """

    is_public = kwargs.get("is_public", False)
    content_type = kwargs.get("content_type")
    meta = kwargs.get("meta")

    if not content_type:
        file_type_guess = mimetypes.guess_type(file_src)

        if not file_type_guess[0]:
            raise Exception("We can't identify content type. Please specify directly via content_type arg.")

        content_type = file_type_guess[0]

    extra_args = {
        "ACL": "public-read" if is_public else "private",
        "ContentType": content_type,
    }

    if isinstance(meta, dict):
        extra_args["Metadata"] = meta

    return spaces_client.upload_file(
        file_src,
        space_name,
        save_as,
        # boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS
        ExtraArgs=extra_args,
    )


def download_file_from_space(spaces_client: str, space_name: str, file_path: str, save_to: str):
    """
    :param spaces_client: Your DigitalOcean Spaces client from get_spaces_client()
    :param space_name: Unique name of your space. Can be found at your digitalocean panel
    :param file_path: Path to your file
    :param save_to: Where to save your file on your disk
    :return:
    """
    spaces_client.download_file(space_name, file_path, save_to)


client = get_spaces_client(
    region_name=env.DO_SPACES_REGION,
    endpoint_url=env.DO_SPACES_ENDPOINT,
    key_id=env.DO_SPACES_KEY,
    secret_access_key=env.DO_SPACES_SECRET,
)
