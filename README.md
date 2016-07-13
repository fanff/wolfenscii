# Wolfenscii

[Wolfenscii](https://github.com/fanff/wolfenscii) is a clone of the venerable Wolfenstein 3D using only ASCII characters for his graphical rendering. Wolfenscii is written in Python 2.

## Minimal documentation


#### To run Wolfenscii:

```bash
python wolfenscii_client.py
```

#### To deploy in docker:

This method allow you to deplay wolfenscii in a container and make it availlable via ssh.

* First build the image
```bash
docker build -t wspim . 
```

* Then run the container 
```bash
docker run -d --name wsp -p 2222:22 wspim
```

* Connect remotely
```bash
ssh -p 2222 wolf@yourhostname 
```

## Example of rendering

![alt text](https://github.com/fauconnier/wolfenscii/raw/master/wolfenscii/asset/pic/pic.png "Graphical rendering")
