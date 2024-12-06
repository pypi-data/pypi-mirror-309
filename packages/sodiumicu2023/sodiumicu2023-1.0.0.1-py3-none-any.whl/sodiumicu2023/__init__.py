import webbrowser
import tempfile, os
import sodiumicu2023.webpage_data as webpage_data
import base64, zlib

def write_data_to(data, dir):
    open(dir, 'wb').write(zlib.decompress(base64.b64decode(data)))

tempfolder = str(tempfile.TemporaryDirectory()).replace('\\', '/')
os.mkdir(f"{tempfolder}/fonts")
write_data_to(webpage_data.index_html, f"{tempfolder}/index.html")
write_data_to(webpage_data.icon_png, f"{tempfolder}/icon.png")
write_data_to(webpage_data.bgm_m4a, f"{tempfolder}/bgm.m4a")
write_data_to(webpage_data.font_file, f"{tempfolder}/fonts/XiaolaiSC-Regular-23w37ver10.woff")

webbrowser.open(f"file://{tempfolder}/index.html")
