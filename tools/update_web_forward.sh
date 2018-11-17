#!/usr/bin/env bash
ADDRESS=$1
ssh maarten-hoogendoorn.nl -i ~/.ssh/google-cloud-shell "echo \"<html><script>window.location='$ADDRESS';</script></html>\" > /var/web/csd.cool/index.html"
