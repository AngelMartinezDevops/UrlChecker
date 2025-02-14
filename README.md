# URL Checker

A command-line tool for checking URLs status, providing detailed information about HTTP status, Application Gateway, and IP addresses.

## Overview

URL Checker is a Python-based tool that allows you to quickly verify the status and gather information about one or multiple URLs. It provides color-coded output for better readability and includes detailed information about redirections and server configurations.

## Features

- 🔍 HTTP status verification with full redirection chain
- 🌐 Application Gateway detection
- 📡 IP address resolution
- 🎨 Color-coded output for better visibility
- 🔄 Multiple URL support in a single command
- ⚡ Fast response time (5 seconds timeout)
- 🔒 HTTPS support by default s

## Installation

### Option 1: Pre-compiled Binaries

Choose the appropriate binary for your system:

- For Intel/AMD processors (x86_64):
  sudo mv urlcheck-amd64 /usr/local/bin/urlcheck

- For Apple Silicon/ARM processors:
  sudo mv urlcheck-arm64 /usr/local/bin/urlcheck

### Option 2: From Source Code

If you prefer to run from the Python source:

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:
   pip install requests colorama
3. Make the script executable:
   chmod +x urlcheck.py

## Usage

Basic syntax:

urlcheck <url1> <url2> <url3> ...

Example:
 urlcheck https://example.com https://example.com/subpage
