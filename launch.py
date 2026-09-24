import subprocess
import sys


def main():
    print()
    print("=" * 60)
    print(" SIGNAL — AI RESUME RANKER")
    print("=" * 60)
    print()
    print("Starting Streamlit product...")
    print()
    print("Open:")
    print("http://localhost:8501")
    print()

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "streamlit_app.py",
        ],
        check=False,
    )


if __name__ == "__main__":
    main()
