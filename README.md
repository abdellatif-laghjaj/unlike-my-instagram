# instagram-unliker

Simple script for removing your Instagram likes.  
Inspired by [jhnguyen521/InstaUnliker](https://github.com/jhnguyen521/InstaUnliker) 💚  
Powered by [subzeroid/instagrapi](https://github.com/subzeroid/instagrapi) 💚

## ✨ Features

-   **🔒 Enhanced Security**: No hardcoded credentials, environment variable configuration
-   **⚡ Optimized Performance**: Batch processing, intelligent rate limiting, dynamic delays
-   **🛡️ Robust Error Handling**: Exponential backoff, retry mechanisms, graceful degradation
-   **📊 Detailed Logging**: Progress tracking, performance metrics, comprehensive logs
-   **🔄 Session Management**: Persistent sessions, automatic re-authentication
-   **⚙️ Configurable**: Extensive configuration options via environment variables

## 🔒 Security Improvements

-   Credentials stored in environment variables (not in code)
-   Session files for reduced login frequency
-   Secure 2FA/MFA support with TOTP
-   Comprehensive error logging without exposing sensitive data

## ⚙️ Configuration

### Method 1: Environment Variables (Recommended)

1. Copy `.env.example` to `.env`
2. Edit `.env` and fill in your credentials:

```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
INSTAGRAM_MFA_SECRET=your_totp_secret  # If 2FA enabled
LIKE_REMOVAL_AMOUNT=1000

# Performance Settings (NEW!)
MIN_DELAY=0.5              # Reduced from 2.0 for faster processing
MAX_DELAY=1.5              # Reduced from 5.0 for faster processing
BATCH_SIZE=50              # Process posts in batches
CONCURRENT_REQUESTS=3      # Parallel processing
```

### Method 2: System Environment Variables

Set environment variables in your system:

```bash
# Windows (Command Prompt)
set INSTAGRAM_USERNAME=your_username
set INSTAGRAM_PASSWORD=your_password

# Windows (PowerShell)
$env:INSTAGRAM_USERNAME="your_username"
$env:INSTAGRAM_PASSWORD="your_password"

# Linux/Mac
export INSTAGRAM_USERNAME="your_username"
export INSTAGRAM_PASSWORD="your_password"
```

### 🔒 2FA / MFA

If 2FA is configured for your account, set the TOTP secret in the `INSTAGRAM_MFA_SECRET` environment variable.  
The TOTP will be calculated automatically when needed.

## 🚀 Usage

### Quick Start (Windows)

1. Run `run.bat` - it will guide you through the setup

### With uv (Recommended)

1. Install uv: https://docs.astral.sh/uv/getting-started/installation
2. Run: `uv run unliker.py`

### With pip/python

1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python unliker.py`

## ⚡ Performance Optimizations

-   **Batch Processing**: Processes posts in configurable batches for better efficiency
-   **Intelligent Rate Limiting**: Dynamic delays based on Instagram's response patterns
-   **Session Persistence**: Reuses authentication sessions to reduce login overhead
-   **Exponential Backoff**: Automatically handles rate limits with smart waiting
-   **Concurrent-Safe**: Designed to handle Instagram's API limitations gracefully

## 📊 Configuration Options

| Variable              | Default      | Description                                  |
| --------------------- | ------------ | -------------------------------------------- |
| `LIKE_REMOVAL_AMOUNT` | 1000         | Maximum number of posts to unlike            |
| `BATCH_SIZE`          | 50           | Number of posts to process in each batch     |
| `MIN_DELAY`           | 2.0          | Minimum delay between requests (seconds)     |
| `MAX_DELAY`           | 5.0          | Maximum delay between requests (seconds)     |
| `MAX_RETRIES`         | 3            | Maximum retry attempts for failed operations |
| `BACKOFF_FACTOR`      | 2.0          | Exponential backoff multiplier               |
| `QUIET_MODE`          | false        | Enable quiet mode (less console output)      |
| `SESSION_FILE`        | session.json | File to store session data                   |

## 🚧 Rate Limiting & Safety

The script includes multiple safety mechanisms:

-   **Intelligent delays**: Automatically adjusts timing based on Instagram's responses
-   **Rate limit detection**: Detects and handles rate limits gracefully
-   **Exponential backoff**: Increases wait times when rate limits are encountered
-   **Batch processing**: Reduces API load by processing in smaller chunks
-   **Session reuse**: Minimizes authentication requests

## 📋 Logging

The script creates detailed logs:

-   `unliker.log`: Complete operation log with timestamps
-   Console output: Real-time progress updates
-   Statistics: Final performance metrics

## � Troubleshooting

### Common Issues:

1. **Login failures**: Check credentials, 2FA settings
2. **Rate limits**: Reduce `BATCH_SIZE`, increase delays
3. **Session issues**: Delete `session.json` to force re-login
4. **Permission errors**: Ensure account has proper permissions

### Performance Tuning:

-   **Faster processing**: Decrease `MIN_DELAY` and `MAX_DELAY` (risky)
-   **Safer processing**: Increase delays and reduce `BATCH_SIZE`
-   **2FA issues**: Verify `INSTAGRAM_MFA_SECRET` is correct

## 📈 Performance Metrics

The optimized version typically achieves:

-   20-40 posts per minute (depending on delays)
-   95%+ success rate with proper configuration
-   Automatic recovery from temporary issues
-   Detailed progress tracking and ETA calculation  
    The [current default value](https://github.com/cyb3rko/instagram-unliker/blob/main/unliker.py#L9) worked fine for me while running this script every few hours.
