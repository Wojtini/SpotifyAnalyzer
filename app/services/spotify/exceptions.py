from requests import Response


class SpotifyAuthError(Exception):
    def __init__(self, response: Response) -> None:
        super().__init__(
            f"{response.status_code} error during receiving token message: {response.text}",
        )


class EnvironmentalVariableDoesNotExistError(Exception):
    def __init__(self, env_var: str) -> None:
        super().__init__(f"Environment variable {env_var} does not exist")


class SpotifyFetchError(Exception):
    def __init__(self, response: Response) -> None:
        super().__init__(
            f"{response.status_code} error during data fetch: {response.text}",
        )
