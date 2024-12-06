from ..core.engine_manager.app_initializer import AppInitializer
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Run the Pypodmanager app.")
    parser.add_argument('--config', type=str, help='Path to the configuration file')
    parser.add_argument('--cwd', type=str, help='Set the current working directory', default=os.getcwd())
    args = parser.parse_args()

    if args.cwd:
        try:
            os.chdir(args.cwd)
            print(f"Changed current working directory to: {args.cwd}")
        except OSError as e:
            print(f"Error changing directory: {e}")
            return

    app = AppInitializer(config_path=args.config, cwd=args.cwd)
    app.run()

if __name__ == "__main__":
    main()