# DeepScript: Write anything in your handwriting
## Steps to run this repo:-

- Upload your handwriting sample as the way given in the repo. Make sure your characters are boldly written.
- Run the segment_char program and make sure to verify the paths in the program.
- Run the pngtosvg.py program. It will create two directories but we need only one i.e svg_output.
### Disclaimer⚠️❗
Before running the finalfont.py program, make sure to rename your .svg files as A.svg, a.svg i.e. character_name.svg. I know its a tedious task to do but I am working on automating this fully. Stay tuned!! 
- Run the finalfont.py program. It will create your font which will be used to render your output.
- Run the textrender.py program. It will give you your ouput.

### Make sure to install these dependencies
```bash
pip install Pillow
pip install fontforge
pip install psMat
```
