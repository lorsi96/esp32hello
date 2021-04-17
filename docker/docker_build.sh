docker build -t pymaketool/esp32 \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) .