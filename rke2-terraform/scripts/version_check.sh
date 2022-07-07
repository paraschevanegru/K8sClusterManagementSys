#!/bin/bash
verTerraform="$(terraform version 2>&1 | awk 'NR==1' | awk '{print $2}')"
versionNeeded="v1.2.3"
if [ ! command -v terraform ] &>/dev/null || [ $verTerraform != $versionNeeded ]; then
    echo "terraform nu a fost gasit sau versiunea utilizata un corespunde cu cea necesara"
    exit
else
    echo "terraform este instalat"
fi
