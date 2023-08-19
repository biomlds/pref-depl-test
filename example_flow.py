import httpx
from prefect import flow, get_run_logger, task
from prefect.deployments import Deployment

# from prefect_aws import AwsCredentials

# aws_credentials_block = AwsCredentials.load("aws-push")


@task
def get_url(url: str, params: dict = None):
    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json()


@flow(retries=3, retry_delay_seconds=5)
def get_repo_info(repo_name: str = "PrefectHQ/prefect"):
    repo = get_url(f"https://api.github.com/repos/{repo_name}")
    logger = get_run_logger()
    logger.info("PrefectHQ/prefect repository statistics 🤓:")
    logger.info(f"Stars 🌠 : {repo['stargazers_count']}")
    logger.info(f"Forks 🍴 : {repo['forks_count']}")

