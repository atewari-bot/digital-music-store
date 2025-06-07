from dotenv import load_dotenv

def load_environment_variables():
    """
    Load environment variables from a .env file.
    """
    load_dotenv(dotenv_path='.env', override=True)
    print("Environment variables loaded successfully.")