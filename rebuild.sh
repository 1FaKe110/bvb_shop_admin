#echo sudo docker build --tag bvb-shop-admin .
sudo docker build --tag bvb-shop-admin .
#echo sudo docker run bvb-shop -p 1111:1111 bvb-shop-admin
sudo docker run -p 1111:1111 bvb-shop-admin
