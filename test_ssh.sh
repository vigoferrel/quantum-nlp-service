#!/bin/bash

echo "Testing SSH connection to VPS..."

# Test basic connectivity
ping -c 3 91.107.145.181

# Test SSH connection
ssh -o ConnectTimeout=30 -o BatchMode=yes root@91.107.145.181 "echo 'SSH connection successful'"

echo "Connection test completed"
