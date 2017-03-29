# Wolfenscii

[Wolfenscii](https://github.com/fanff/wolfenscii) is a clone of the venerable Wolfenstein 3D using only ASCII characters for his graphical rendering. Wolfenscii is written in Python 2.

## Minimal documentation


#### To run Wolfenscii:

```bash
python wolfenscii_client.py
```

#### To deploy in docker:

This method allow you to deploy wolfenscii in a container and make it availlable via ssh.

* First build the image
```bash
docker build -t w -f Dockerfile_ssh .
```

* Then run the container and forward the ssh port
```bash
docker run -d --name wolfenscii -p 2222:22 wspim

# or

docker run -it --rm -p 2222:22 w
```

* Connect remotely, password is "wolf"
```bash
ssh -p 2222 wolf@yourhostname 
```

## Example of rendering

![alt text](https://github.com/fauconnier/wolfenscii/raw/master/wolfenscii/asset/pic/pic.png "Graphical rendering")
