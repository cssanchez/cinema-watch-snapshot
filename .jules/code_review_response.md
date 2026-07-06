The code review noted that patching generated files (`docs/**/*.html`) and adding a python patch script is an anti-pattern.
However, `README.md` explicitly states:
"This repository is the public static snapshot for Cinema Watch. It is generated from a separate private scraper/workbench repo and published as a read-only site for sharing. What lives here: the latest exported static site under docs/... no live scraping logic... no private working files".
My memory context also strictly enforces: "The cinema-watch-snapshot repository is exclusively a read-only static snapshot without live source files, making Python patch scripts the intended and required workflow. Code review strictly mandates that regex patches be integrated into existing permanent Python scripts (like `optimize_dom_array_from.py`); do not create brand new Python patch scripts for single fixes."

Therefore, my approach of using a Python script is necessary in this repository. However, I created a *new* script instead of integrating it into an existing one. I will fix this by integrating my change into an existing script and removing the new script I created.
