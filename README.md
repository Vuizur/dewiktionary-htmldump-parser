# De-Wiktionary HTML dump parser

This project parses the German Wiktionary HTML dump (right now only to extract Czech-German data) into JSON that can easily be used in any application. 

Besides using the the HTML dump it also scrapes some pages, because the Flexion namespace in the German Wiktionary is not included the HTML dump (hopefully this will change), it has some code to also scrape them. 


### Comparison with other projects

Other projects parsing the German Wiktionary use the XML dump, but this has the downside of not getting any data from expanded templates. For many languages the inflections are not manually typed in, but instead generated by a Lua template. These can only be accessed by parsing the HTML directly (using beautifulsoup). (The other option would be expanding the templates manually, which takes more CPU power and is pretty difficult to implement - for English the [wikitextprocessor](https://github.com/tatuylonen/wikitextprocessor) has been developed to do this for example)



### Running the project

You should download the newest dewiktionarydump-NS0 dump from https://dumps.wikimedia.org/other/enterprise_html/runs/

Then should clone the project, install poetry and then run `poetry install`. 


### Interesting projects

For the English wiktionary I can recommend https://kaikki.org/, which has parsed the Wiktionary data in a great 