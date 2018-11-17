DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/v1
cd $DIR
make build
make push
make deploy
