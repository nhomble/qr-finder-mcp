# qr-finder

play with mcps and find qr codes appearing on my screen

## Local Installation

```
UV_PATH=$(which uv)
git clone https://github.com/nhomble/qr-finder-mcp .
INSTALL_PATH=$(pwd)
```

Given the variables above: 

```
{
  "mcpServers": {
    "qr-finder": {
      "command": "$UV_PATH",
      "args": [
        "--directory",
        "$INSTALL_PATH",
        "run",
        "server.py"
      ]
    }
  }
}
```