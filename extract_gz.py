import gzip, shutil, pathlib
for gz in sorted(pathlib.Path(__file__).resolve().parent.glob("*.gz")):
    out = gz.with_suffix("")
    with gzip.open(gz, "rb") as src, open(out, "wb") as dst:
        shutil.copyfileobj(src, dst)
    print(gz.name, "->", out.name)
print("done")
