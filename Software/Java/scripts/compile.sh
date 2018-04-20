#/usr/bin/env bash
mkdir -p ./bin
javac -d ./bin -classpath .:classes:/opt/pi4j/lib/'*' ./src/com/dexterind/gopigo/*.java ./src/com/dexterind/gopigo/behaviours/*.java ./src/com/dexterind/gopigo/components/*.java ./src/com/dexterind/gopigo/events/*.java ./src/com/dexterind/gopigo/utils/*.java ./test/tests/*.java ./test/*.java;