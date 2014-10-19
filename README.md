Vademecum Parser
====================
Small phython utility to parse [Professor Mañas](http://www.dit.upm.es/~pepe/)' Java [Vademecum](http://www.dit.upm.es/~pepe/libros/vademecum/index.html) into a json format for [calista-bot](https://github.com/gsi-upm/calista-bot)

***WARNING: This is development level software.  Please do not use it unless you
             are familiar with what that means and are comfortable using that type
             of software.***

Portability
---------------------------------------

This is mostly a python script (parser.py) I used to web-scrapp the data from the vademecum to a custom json format. Is not a good script, and I don't think it  is really portable. As future work, I plan on changing it to use an actual scrapper, and to write the data to LOM, but I cannot guarantee I'll be able to do it.

Dependencies and Usage
---------------------------------------
You just need python, a Firefox-like browser (I use Iceweasel), and a couple of libaries:

    pip install selenium unidecode

You will also need the "native2ascii" tool, which should come with the openjdk-7-java package.

Just run "run.sh", in the same directory, and it should generate the "vademecum_encoded.json" file, with the data, and "dictionary.txt", a dictionary to be compiled with [Unitex](http://www-igm.univ-mlv.fr/~unitex/)

License
---------------------------------------
Copyright 2014 Alberto Mardomingo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


