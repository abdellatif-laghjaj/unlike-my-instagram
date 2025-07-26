import os
import pyotp
import time
import signal
import sys
from datetime import datetime
from dotenv import load_dotenv
from instagrapi import Client
from pathlib import Path

# Load environment variables
load_dotenv()

# =======================================
# Configuration from environment variables
# =======================================

like_removal_amount = int(os.getenv("LIKE_REMOVAL_AMOUNT", 1000))
quiet_mode = os.getenv("QUIET_MODE", "false").lower() == "true"
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")
mfa_secret = os.getenv("INSTAGRAM_MFA_SECRET", "")

# =======================================

output = ""
should_terminate = False


def get_timestamp():
    """Get current timestamp in [HH:MM:SS] format"""
    return datetime.now().strftime("[%H:%M:%S]")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global should_terminate

    println("\n⚠️  Ctrl+C detected! Do you want to terminate the script?")
    try:
        response = input(f"{get_timestamp()} [Y/n]: ").strip().lower()
        if response in ["y", "yes", ""]:
            println("🛑 Script termination requested by user.")
            should_terminate = True
        else:
            println("▶️  Continuing script execution...")
    except KeyboardInterrupt:
        # If user presses Ctrl+C again during the prompt
        println("\n🛑 Force termination requested. Exiting...")
        sys.exit(0)


def validate_env_vars():
    """Validate required environment variables"""
    if not username:
        println("❌ INSTAGRAM_USERNAME not found in .env file!")
        exit(1)
    if not password:
        println("❌ INSTAGRAM_PASSWORD not found in .env file!")
        exit(1)
    println("✅ Environment variables loaded successfully")


def init_client() -> Client:
    settings_file = "session.json"
    client = Client()
    client.delay_range = [1, 3]

    if not os.path.isfile(settings_file):
        println("📄 Settings file not found, creating one on the fly...")
        println("🔐 Logging in via username and password...")
        if mfa_secret and mfa_secret != "":
            totp = pyotp.TOTP(mfa_secret).now()
            println(f"🔑 Configured TOTP MFA with code '{totp}'")
            client.login(username, password, verification_code=totp)
        else:
            client.login(username, password)
        client.dump_settings(Path("session.json"))
        println("💾 Session saved successfully!")
    else:
        println("🔄 Session found, reusing login...")
        client.load_settings(Path("session.json"))
        client.login(username, password)
        println("✅ Login successful!")

    return client


def unlike(client: Client):
    global should_terminate
    removed = 0
    println(f"🎯 Target: Remove {like_removal_amount} liked posts")

    while removed < like_removal_amount and not should_terminate:
        # Check for termination request
        if should_terminate:
            println(
                f"🛑 Script terminated by user. Unliked {removed} posts before termination."
            )
            break

        liked = client.liked_medias()
        count_reached = False

        println("🚀 Beginning deletion of liked posts...")

        for post in liked:
            # Check for termination request before each operation
            if should_terminate:
                println(
                    f"🛑 Script terminated by user. Unliked {removed} posts before termination."
                )
                return

            start_time = time.time()
            try:
                client.media_unlike(post.id)
                end_time = time.time()
                execution_time = round(end_time - start_time, 2)
                removed += 1
                println(
                    f"✅ {removed}: Unliked post {post.id} by @{post.user.username} ({execution_time}s)"
                )
            except Exception as e:
                end_time = time.time()
                execution_time = round(end_time - start_time, 2)
                println(
                    f"❌ Failed to unlike post {post.id} by @{post.user.username} ({execution_time}s)"
                )
                println("⚠️ Rate limit most likely reached. Try again soon.")
                println(f"📊 Deleted {removed} liked posts.")
                println("🔍 Exception details:")
                println(str(e))
                print(output)
                return

            if removed >= like_removal_amount:
                count_reached = True
                break

        if not count_reached and not should_terminate:
            println("📥 Grabbing more posts...")
            liked = client.liked_medias()

            result_count = len(liked)
            println(f"📊 Grabbed {result_count} more posts.")
            if result_count == 0:
                println("🎉 No more posts to unlike!")
                println(f"✅ Successfully deleted {removed} liked posts.")
                break

    if not should_terminate:
        println(f"🏁 Finished deleting {removed} liked posts!")
    else:
        println(f"🛑 Script terminated. Final count: {removed} posts unliked.")


def println(line):
    """Enhanced logging function with timestamp and emoji support"""
    timestamped_line = f"{get_timestamp()} {line}"
    if quiet_mode:
        global output
        output += f"\n{timestamped_line}"
    else:
        print(timestamped_line)


def main():
    global should_terminate

    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    println("🤖 Instagram Unlike Bot Started")
    println("💡 Press Ctrl+C to safely terminate the script at any time")
    println("=" * 60)

    # Validate environment variables
    validate_env_vars()

    println(f"👤 Username: {username}")
    println(f"🎯 Like removal target: {like_removal_amount}")
    println(f"🔇 Quiet mode: {'ON' if quiet_mode else 'OFF'}")
    println("=" * 60)

    try:
        client = init_client()
        unlike(client)

        if not should_terminate:
            println("🎉 Script completed successfully!")
        else:
            println("🛑 Script was terminated by user request.")

    except Exception as e:
        println(f"💥 Script failed with error: {str(e)}")
        if not quiet_mode:
            raise


if __name__ == "__main__":
    main()
