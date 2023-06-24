docker build . -t gp_dev
docker run --privileged -v /mnt/nvme0n1/gp:/data/gp --name gp_dev -t -i gp_dev
