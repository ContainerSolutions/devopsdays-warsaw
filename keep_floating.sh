#!/usr/bin/env bash
#dev="HID 04d9:a02a"
dev="SEM Trust Numpad"

while true; do
  if xinput | grep -q "$dev"; then
    if ! xinput | grep  "$dev" | grep -q floating; then
      date
      echo "Make it float again!"

      xinput float "$dev"
      xinput float "keyboard:$dev"
    fi
  fi
  sleep 0.5
done
