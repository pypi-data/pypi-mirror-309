import contextlib
import json
import logging
import os
import pathlib
import threading
from collections.abc import Mapping

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def patch_environment(**kwargs):
    """Temporarily patch environment variables.

    Args:
        **kwargs: Key-value pairs of environment variables to set.

    Yields:
        None
    """
    original = {}
    try:
        for key, value in kwargs.items():
            if value is None:
                original[key] = os.environ.pop(key, None)
                continue
            original[key] = os.environ.get(key)
            os.environ[key] = value
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def run_server(
    host: str = "127.0.0.1",
    port: int = 2024,
    reload: bool = False,
    graphs: dict | None = None,
    n_jobs_per_worker: int | None = None,
    env_file: str | None = None,
    open_browser: bool = False,
    debug_port: int | None = None,
    env: str | pathlib.Path | Mapping[str, str] | None = None,
):
    """Run the LangGraph API server."""
    import uvicorn

    env_vars = env if isinstance(env, Mapping) else None
    if isinstance(env, str | pathlib.Path):
        try:
            from dotenv.main import DotEnv

            env_vars = DotEnv(dotenv_path=env).dict()
            logger.debug(f"Loaded environment variables from {env}: {sorted(env_vars)}")

        except ImportError:
            logger.warning(
                "python_dotenv is not installed. Environment variables will not be available."
            )

    if debug_port is not None:
        try:
            import debugpy
        except ImportError:
            logger.warning("debugpy is not installed. Debugging will not be available.")
            logger.info("To enable debugging, install debugpy: pip install debugpy")
            return
        debugpy.listen((host, debug_port))
        logger.info(
            f"🐛 Debugger listening on port {debug_port}. Waiting for client to attach..."
        )
        logger.info("To attach the debugger:")
        logger.info("1. Open your python debugger client (e.g., Visual Studio Code).")
        logger.info(
            "2. Use the 'Remote Attach' configuration with the following settings:"
        )
        logger.info("   - Host: 0.0.0.0")
        logger.info(f"   - Port: {debug_port}")
        logger.info("3. Start the debugger to connect to the server.")
        debugpy.wait_for_client()
        logger.info("Debugger attached. Starting server...")

    local_url = f"http://{host}:{port}"
    studio_url = f"https://smith.langchain.com/studio/?baseUrl={local_url}"

    def _open_browser():
        import time
        import urllib.request
        import webbrowser

        while True:
            try:
                with urllib.request.urlopen(f"{local_url}/ok") as response:
                    if response.status == 200:
                        webbrowser.open(studio_url)
                        return
            except urllib.error.URLError:
                pass
            time.sleep(0.1)

    welcome = f"""

        Welcome to

╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: \033[36m{local_url}\033[0m
- 🎨 Studio UI: \033[36m{studio_url}\033[0m
- 📚 API Docs: \033[36m{local_url}/docs\033[0m

This in-memory server is designed for development and testing.
For production use, please use LangGraph Cloud.

"""
    logger.info(welcome)
    with patch_environment(
        MIGRATIONS_PATH="__inmem",
        DATABASE_URI=":memory:",
        REDIS_URI="fake",
        N_JOBS_PER_WORKER=str(n_jobs_per_worker if n_jobs_per_worker else 1),
        LANGSERVE_GRAPHS=json.dumps(graphs) if graphs else None,
        LANGSMITH_LANGGRAPH_API_VARIANT="test",
        **env_vars,
    ):
        if open_browser:
            threading.Thread(target=_open_browser, daemon=True).start()

        uvicorn.run(
            "langgraph_api.server:app",
            host=host,
            port=port,
            reload=reload,
            env_file=env_file,
            access_log=False,
            log_config={
                "version": 1,
                "incremental": False,
                "disable_existing_loggers": False,
                "formatters": {
                    "simple": {"class": "langgraph_api.base.shared.logging.Formatter"}
                },
                "handlers": {
                    "console": {
                        "class": "logging.StreamHandler",
                        "formatter": "simple",
                        "stream": "ext://sys.stdout",
                    }
                },
                "root": {"handlers": ["console"]},
            },
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="CLI entrypoint for running the LangGraph API server."
    )
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=2024, help="Port to bind the server to"
    )
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    parser.add_argument(
        "--config", default="langgraph.json", help="Path to configuration file"
    )
    parser.add_argument(
        "--n-jobs-per-worker",
        type=int,
        help="Number of jobs per worker. Default is None (meaning 10)",
    )
    parser.add_argument(
        "--no-browser", action="store_true", help="Disable automatic browser opening"
    )
    parser.add_argument(
        "--debug-port", type=int, help="Port for debugger to listen on (default: none)"
    )

    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config_data = json.load(f)

    graphs = config_data.get("graphs", {})
    run_server(
        args.host,
        args.port,
        not args.no_reload,
        graphs,
        n_jobs_per_worker=args.n_jobs_per_worker,
        open_browser=not args.no_browser,
        debug_port=args.debug_port,
        env=config_data.get("env", None),
    )


if __name__ == "__main__":
    main()
