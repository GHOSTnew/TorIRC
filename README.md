[![Licence GPLv3](http://img.shields.io/badge/license-GPLv3-yellow.svg)](http://www.gnu.org/licenses/quick-guide-gplv3.fr.html)

# TorIRC

## Dépendances:
* [SocksiPy](http://socksipy.sourceforge.net/)
* Python __2.7__

## Utilisation:
Remplacez le __.onion__ du fichier TorIRC.py à la ligne [__132__](https://github.com/GHOSTnew/TorIRC/blob/master/TorIRC.py#L132) 
par celui du serveur sur lequel vous souhaitez vous connecter

Lancez le script:
```
$ python TorIRC.py
```

Puis connectez vous sur __127.0.0.1__ et le port __20000__

Exemple avec [irssi](http://irssi.org/):
```
$ irssi -c 127.0.0.1 -p 20000
```