#!/bin/bash
set -e
clear
/opt/homebrew/bin/uvx --offline --from "mcpforunityserver==9.7.1" mcp-for-unity --transport http --http-url http://127.0.0.1:8080 --project-scoped-tools --pidfile "/Users/max/KSU/labs/Virtual and augmented reality technologies/PhysicsAR/Library/MCPForUnity/RunState/mcp_http_8080.pid" --unity-instance-token 8ebecbeae9d9406c8a8d990a28d55a78
