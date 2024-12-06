# py-long-s
This Python tool accurately inserts the historical long S character (&nbsp;&#x17F;&nbsp;) back into the given text to make it appear as if it were written before the 20th century.

English, French, German, Spanish, and Italian are supported.

#### Installation
```
pip install long-s
```
<br>

The libraries used in this project can be installed separately by using:
```
pip install numpy python-docx odfpy unidecode
```

<br>

## Online Converter
There's also a [JavaScript version](https://github.com/travisgk/long-s-converter) available that can be used online.

<br>

## Example
```
import long_s

print(long_s.convert("The discussion was surprisingly insightful.", lang="en"))
print(long_s.convert("La discussion était étonnamment perspicace.", lang="fr"))
print(long_s.convert("Die Diskussion war überraschend aufschlussreich.", lang="de"))
print(long_s.convert("La discusión fue sorprendentemente perspicaz.", lang="es"))
print(long_s.convert("La discussione è stata sorprendentemente perspicace.", lang="it"))
```

```
The di&#x17F;cu&#x17F;&#x17F;ion was &#x17F;urpri&#x17F;ingly in&#x17F;ightful.
La di&#x17F;cu&#x17F;&#x17F;ion était étonnamment per&#x17F;picace.
Die Disku&#x17F;&#x17F;ion war überra&#x17F;chend auf&#x17F;chlu&#x17F;sreich.
La di&#x17F;cu&#x17F;ión fue &#x17F;orprendentemente per&#x17F;picaz.
La di&#x17F;cu&#x17F;&#x17F;ione è &#x17F;tata &#x17F;orprendentemente per&#x17F;picace.
```

<br>

## Converting Files
### .txt files
```
long_s.convert_text_file(src_path="story.txt", dst_path=None, lang="en"))
```
Since `dst_path` is None, the program will save the converted text file as `story-long-s.txt`.

<br>

### .odf files
```
long_s.convert_odf_file(src_path="story.odt", dst_path="old-story.odt", lang="en"))
```

<br>

### .docx files
```
long_s.convert_docx_file(src_path="märschen.docx", lang="de"))
```

<br>

## Special Thanks

Thank you Andrew West of the TeX Users Group for the documentation found under [The Rules for Long S](https://www.tug.org/TUGboat/tb32-1/tb100west.pdf), which was fundamental in writing the conversion functions for English, French, Spanish, and Italian. 
