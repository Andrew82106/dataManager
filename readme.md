# How to use

打包成docker即可。

```shell notranslate position-relative overflow-auto
sudo docker build -f ./dockerfile -t dtm:v0 .
docker run -d -p 9990:3690 dtm:v0
```
