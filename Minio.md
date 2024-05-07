# To get Minio Running run the following Command:

# docker run -d -p 9000:9000 -p 9001:9001 --name minio -e "MINIO_ROOT_USER=Admin" -e "MINIO_ROOT_PASSWORD=Password" -v /mnt/data:/data --restart=always quay.io/minio/minio server /data --console-address ":9001"