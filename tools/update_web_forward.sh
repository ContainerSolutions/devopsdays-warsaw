#!/usr/bin/env bash
ADDRESS=$1
ssh maarten-hoogendoorn.nl "echo \"<html><script>window.location='$ADDRESS';</script></html>\" > /var/web/csd.cool/index.html"
