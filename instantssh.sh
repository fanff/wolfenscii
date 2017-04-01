

docker build -t w -f Dockerfile_ssh . 
docker run -d --name wolf -p 2222:22 w 

echo "ssh -p 2222 wolf@localhost"

